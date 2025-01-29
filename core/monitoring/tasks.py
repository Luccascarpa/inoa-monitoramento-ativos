# using celery as scheduler

from celery import shared_task
from .models import Asset
from .utils import check_and_save_price



@shared_task
def check_prices_periodically():
    # Task for checking the price of all assets
    for asset in Asset.objects.all(): check_and_save_price(asset)