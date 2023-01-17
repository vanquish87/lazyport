from django.contrib import admin
from .models import Stock, Stock_price

# Register your models here.
class StockAdmin(admin.ModelAdmin):
    readonly_fields = ('scriptid', 'exchange')


class Stock_price_Admin(admin.ModelAdmin):
    readonly_fields = ('stock', 'date', 'closing_price')

admin.site.register(Stock, StockAdmin)

admin.site.register(Stock_price, Stock_price_Admin)