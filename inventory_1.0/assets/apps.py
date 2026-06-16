"""
App configuration for the assets app.

This module contains the application configuration class.
"""

from django.apps import AppConfig


class AssetsConfig(AppConfig):
    """Configuration class for the assets application."""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'assets'
