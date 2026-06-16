"""
Admin configuration for the assets app.

Register models here to make them accessible in Django admin panel.
"""

from django.contrib import admin
from .models import Asset, AssetHistory


# Customize Asset admin display
@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    list_display = ('asset_id', 'asset_name', 'asset_type', 'assigned_to', 'status', 'assigned_date')
    list_filter = ('status', 'asset_type', 'assigned_date')
    search_fields = ('asset_id', 'asset_name', 'assigned_to')


# Customize AssetHistory admin display
@admin.register(AssetHistory)
class AssetHistoryAdmin(admin.ModelAdmin):
    list_display = ('get_asset_id', 'changed_by', 'change_type', 'field_changed', 'changed_at')
    list_filter = ('change_type', 'changed_at')
    search_fields = ('asset__asset_id', 'changed_by')
    readonly_fields = ('asset', 'changed_by', 'change_type', 'field_changed', 'old_value', 'new_value', 'changed_at', 'notes')

    @admin.display(description='Asset ID')
    def get_asset_id(self, obj):
        """Display the actual asset_id field from Asset model, not the FK id."""
        return obj.asset.asset_id

