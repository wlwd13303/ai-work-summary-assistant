# 确保应用启动时加载celery app
from .celery import app as celery_app

__all__ = ("celery_app",)
