from django.urls import path
from . import views

urlpatterns = [
    path('', views.asset_list, name='asset_list'),
    path('create/', views.asset_create, name='asset_create'),
    path('edit/<int:asset_id>/', views.asset_edit, name='asset_edit'),
    path('delete/<int:asset_id>/', views.asset_delete, name='asset_delete'),
    path('history/<int:asset_id>/', views.price_history, name='price_history'),
    path('alert-emails/', views.alert_emails_list, name='alert_emails_list'),
    path('alert-emails/create/', views.alert_emails_create, name='alert_emails_create'),
    path('alert-emails/delete/<int:email_id>/', views.alert_email_delete, name='alert_email_delete'),
]