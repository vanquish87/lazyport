from django.contrib import admin
from .models import Stock

# Register your models here.
class StockAdmin(admin.ModelAdmin):
    readonly_fields = ('scriptid', 'exchange')

admin.site.register(Stock, StockAdmin)
