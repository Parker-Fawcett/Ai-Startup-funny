"""Application configuration."""

from django.apps import AppConfig


class CoreConfig(AppConfig):
    """Django app registration for the PumpRun core."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "core"
