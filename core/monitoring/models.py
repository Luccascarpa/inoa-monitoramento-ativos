from django.db import models
from datetime import datetime
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.

class Asset (models.Model):
    # Model to store assets the user wants to track
    name = models.CharField("Asset Name", max_length=100)
    symbol = models.CharField("Asset Symbol", max_length=10, unique=True)
    inferior_limit = models.DecimalField("Lower Limit", max_digits=10, decimal_places=2)
    superior_limit = models.DecimalField("Upper Limit",max_digits=10, decimal_places=2)
    frequency = models.PositiveIntegerField("Checking frequency (minutes)", default=5)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.symbol} - {self.name}'
    
@receiver(post_save, sender=Asset)
def update_tasks_on_change(sender, instance, **kwargs):
    # When an asset is created or updated, the frequency will be adjusted on celery
    from .tasks import create_or_update_periodic_tasks
    create_or_update_periodic_tasks()

class PriceHistory(models.Model):
    # Model to store the price history of the assets being tracked
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    price = models.DecimalField("Price", max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField("Price timestamp",auto_now_add=True)

    def __str__(self):
        return f'{self.asset.symbol} at {self.timestamp} = R${self.price}'