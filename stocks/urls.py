from django.urls import path
from . import views


urlpatterns = [
    path('add-stock/', views.add_stock, name='add-stock'),
    path('search/', views.search_stock, name='search-stock'),
    path('search-list/', views.search_list, name='search-list'),
    path('stock-price-start/', views.stock_price_start, name='stock-price-start'),
    path('stock-price-update/', views.stock_price_update, name='stock-price-update'),
    path('chart/<int:stock_id>/<str:scriptid>/', views.stock_chart, name='stock-chart'),
]