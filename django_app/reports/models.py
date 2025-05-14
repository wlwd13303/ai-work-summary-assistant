from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


class DailyReport(models.Model):
    """日报模型"""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="daily_reports", verbose_name=_("用户")
    )
    date = models.DateField(_("日期"))
    completed_tasks = models.TextField(_("已完成工作"), blank=True)
    planned_tasks = models.TextField(_("计划工作"), blank=True)
    issues = models.TextField(_("遇到的问题"), blank=True)
    notes = models.TextField(_("备注"), blank=True)
    created_at = models.DateTimeField(_("创建时间"), auto_now_add=True)
    updated_at = models.DateTimeField(_("更新时间"), auto_now=True)

    class Meta:
        verbose_name = _("日报")
        verbose_name_plural = _("日报")
        unique_together = ("user", "date")
        ordering = ["-date"]

    def __str__(self):
        return f"{self.user.username}的日报 ({self.date})"


class WeeklyReport(models.Model):
    """周报模型"""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="weekly_reports", verbose_name=_("用户")
    )
    year = models.IntegerField(_("年份"))
    week_number = models.IntegerField(_("周数"))
    start_date = models.DateField(_("开始日期"))
    end_date = models.DateField(_("结束日期"))
    content = models.TextField(_("内容"), blank=True)
    achievements = models.TextField(_("本周成果"), blank=True)
    plans = models.TextField(_("下周计划"), blank=True)
    issues = models.TextField(_("遇到的问题"), blank=True)
    thoughts = models.TextField(_("工作心得"), blank=True)
    created_at = models.DateTimeField(_("创建时间"), auto_now_add=True)
    updated_at = models.DateTimeField(_("更新时间"), auto_now=True)

    class Meta:
        verbose_name = _("周报")
        verbose_name_plural = _("周报")
        unique_together = ("user", "year", "week_number")
        ordering = ["-year", "-week_number"]

    def __str__(self):
        return f"{self.user.username}的周报 ({self.year}年第{self.week_number}周)"
