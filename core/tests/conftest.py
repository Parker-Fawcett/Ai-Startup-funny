"""Shared pytest fixtures: an organization and a logged-in owner client."""

import pytest
from django.contrib.auth.models import User
from django.test import Client

from core.models import Organization


@pytest.fixture(autouse=True)
def _unhashed_static(settings):
    """Keep tests independent of any collectstatic manifest snapshot."""
    settings.STORAGES["staticfiles"]["BACKEND"] = (
        "django.contrib.staticfiles.storage.StaticFilesStorage"
    )


@pytest.fixture
def org() -> Organization:
    return Organization.objects.create(name="Test Septic")


@pytest.fixture
def user(db):
    return User.objects.create_superuser("owner", "owner@example.com", "pw12345!!")


@pytest.fixture
def client(client: Client, user: User) -> Client:
    client.force_login(user)
    return client
