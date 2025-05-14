from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

app_name = "reports"

router = DefaultRouter()
router.register(r"daily", views.DailyReportViewSet, basename="daily_report")
router.register(r"weekly", views.WeeklyReportViewSet, basename="weekly_report")

urlpatterns = [
    path("", include(router.urls)),
]
