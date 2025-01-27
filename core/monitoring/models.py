from django.db import models
from datetime import datetime

# Create your models here.

class Asset (models.Model):
    # Model to store assets the user wants to track
    name = models.CharField("Asset Name", max_length=100)
    symbol = models.CharField("Asset Symbol", max_length=10, unique=True)
    inferior_limit = models.DecimalField("Lower Limit", max_digits=10, decimal_places=2)
    superior_limit = models.DecimalField("Upper Limit",max_digits=10, decimal_places=2)
    frequency = models.DecimalField("Checking frequency (minutes)", blank=True,null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.symbol} - {self.name}'

class PriceHistory(models.Model):
    # Model to store the price history of the assets being tracked
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    price = models.FloatField("Price", max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField("Price timestamp",auto_now_add=True)

    def __str__(self):
        return f'{self.asset.symbol} at {self.timestamp} = R${self.price}'