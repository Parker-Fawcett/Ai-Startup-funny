"""Template helpers for inlining static assets into rendered pages."""

from functools import lru_cache
from pathlib import Path

from django import template
from django.contrib.staticfiles import finders

register = template.Library()


@lru_cache(maxsize=32)
def _read(path: str) -> str:
    found = finders.find(path)
    return Path(str(found)).read_text() if found else ""


@register.simple_tag
def inline_static(path: str) -> str:
    """Return a static file's content so CSS can be inlined without a request."""
    return _read(path)
