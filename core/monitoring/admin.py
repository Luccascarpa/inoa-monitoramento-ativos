from django.contrib import admin

# Register your models here.
from .models import Asset, PriceHistory

#admin.site.register(Asset)
#admin.site.register(PriceHistory)

from django.contrib import admin
from .models import Asset, PriceHistory

@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    list_display = ('symbol', 'name', 'inferior_limit', 'superior_limit', 'frequency')

@admin.register(PriceHistory)
class PriceHistoryAdmin(admin.ModelAdmin):
    list_display = ('asset', 'price', 'timestamp')
