# using celery as scheduler

from celery import shared_task

from django_celery_beat.models import PeriodicTask, IntervalSchedule
import json


@shared_task
def check_all_assets():
    from .models import Asset
    from .utils import check_and_save_price
    """Executa `check_and_save_price` para todos os ativos cadastrados."""
    assets = Asset.objects.all()
    for asset in assets:
        check_and_save_price(asset)


#@shared_task
#def check_prices_periodically():
#    from .models import Asset
#    from .utils import check_and_save_price
    # Task for checking the price of all assets
#    for asset in Asset.objects.all(): check_and_save_price(asset)

@shared_task
def check_asset_price(asset_id):
    # Task to check each an assets price
    from .models import Asset
    from .utils import check_and_save_price
    
    try:
        asset = Asset.objects.get(id=asset_id)
        check_and_save_price(asset)
        print(f"Preço do ativo {asset.symbol} ({asset_id}) verificado com sucesso.")
    except Asset.DoesNotExist:
        print(f"Erro: Ativo com ID {asset_id} não encontrado.")


def create_or_update_periodic_tasks():
    # Create/update periodic tasks oo Celery Beat for each asset
    from .models import Asset
    from django_celery_beat.models import PeriodicTask, IntervalSchedule
    import json

    for asset in Asset.objects.all():
        schedule, _ = IntervalSchedule.objects.get_or_create(
            every=asset.frequency,
            period=IntervalSchedule.MINUTES
        )
        task_name = f'check_asset_{asset.id}'
        PeriodicTask.objects.update_or_create(
            name=task_name,
            defaults={
                "interval": schedule,
                "task": "monitoring.tasks.check_asset_price",
                "args": json.dumps([asset.id]),
                "enabled": True
            }
        )

    # Remover tasks de ativos que não existem mais
    asset_ids = Asset.objects.values_list('id', flat=True)
    PeriodicTask.objects.exclude(name__in=[f'check_asset_{id}' for id in asset_ids]).delete()

    print("✅ Periodic tasks criadas/atualizadas com sucesso!")
