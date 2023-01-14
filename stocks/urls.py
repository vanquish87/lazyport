from django.urls import path
from . import views


urlpatterns = [
    path('add-stock/', views.add_stock, name='add-stock'),
    path('search/', views.search_stock, name='search-stock'),
    path('search-list/', views.search_list, name='search-list'),
]