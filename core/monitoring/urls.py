from django.urls import path
from . import views

urlpatterns = [
    path('', views.asset_list, name='asset_list'),
    path('create/', views.asset_create, name='asset_create'),
    path('edit/<int:asset_id>/', views.asset_edit, name='asset_edit'),
    path('delete/<int:asset_id>/', views.asset_delete, name='asset_delete'),
    path('history/<int:asset_id>/', views.price_history, name='price_history'),
]