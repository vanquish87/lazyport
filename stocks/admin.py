from django.contrib import admin
from .models import Stock, Stock_price

# Register your models here.
class StockAdmin(admin.ModelAdmin):
    readonly_fields = ('scriptid', 'exchange')

admin.site.register(Stock, StockAdmin)

admin.site.register(Stock_price)