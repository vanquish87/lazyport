from django.urls import path
from . import views


urlpatterns = [
    path('add-stock/', views.add_stock, name='add-stock'),
]