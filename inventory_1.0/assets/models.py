"""
Models for the assets app.

This module defines the database structure for storing asset information.
"""

from django.db import models
from django.utils import timezone


class Asset(models.Model):
    """Model to store asset information."""
    asset_id = models.CharField(max_length=50, unique=True)
    asset_name = models.CharField(max_length=100)
    asset_type = models.CharField(max_length=50)
    assigned_to = models.CharField(max_length=100)
    status = models.CharField(max_length=20, default='Available')
    assigned_date = models.DateField(default=timezone.now)

    def __str__(self):
        return self.asset_name


class AssetHistory(models.Model):
    """Model to track all changes made to assets (audit log)."""
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE, related_name='history')
    changed_by = models.CharField(max_length=100)
    change_type = models.CharField(max_length=50)  # Created, Updated, Transferred, Deleted
    field_changed = models.CharField(max_length=50, blank=True)
    old_value = models.CharField(max_length=200, blank=True)
    new_value = models.CharField(max_length=200, blank=True)
    changed_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['-changed_at']  # Most recent first
        verbose_name_plural = 'Asset histories'

    def __str__(self):
        return f"{self.asset.asset_id} - {self.change_type} by {self.changed_by}"

