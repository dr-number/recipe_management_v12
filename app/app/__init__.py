from app.settings import IS_WNDOWS

if not IS_WNDOWS:
    from .celery import app as celery_app
    __all__ = ('celery_app',)