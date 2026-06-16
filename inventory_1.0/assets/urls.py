"""
URL configuration for the assets app.

This module defines all URL patterns for asset-related pages.
"""

from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('assets/', views.asset_list, name='asset_list'),
    path('assets/export/', views.export_assets_csv, name='export_assets'),
    path('add/', views.add_asset, name='add_asset'),
    path('delete/<int:asset_id>/', views.delete_asset, name='delete_asset'),
    path('edit/<int:asset_id>/', views.edit_asset, name='edit_asset'),
    path('history/<int:asset_id>/', views.asset_history, name='asset_history'),
    path('change-password/', auth_views.PasswordChangeView.as_view(template_name='change_password.html'), name='change_password'),
    path('change-password/done/', auth_views.PasswordChangeDoneView.as_view(template_name='change_password_done.html'), name='password_change_done'),

]
