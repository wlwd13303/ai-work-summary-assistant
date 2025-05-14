import logging
from datetime import timedelta

from django.utils import timezone
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import DailyReport, WeeklyReport
from .serializers import (
    DailyReportSerializer,
    WeeklyReportGenerateSerializer,
    WeeklyReportSerializer,
)
from .tasks import generate_weekly_report_task

logger = logging.getLogger(__name__)


class DailyReportViewSet(viewsets.ModelViewSet):
    """日报视图集"""

    serializer_class = DailyReportSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """只返回当前用户的日报"""
        return DailyReport.objects.filter(user=self.request.user)

    @action(detail=False, methods=["get"])
    def this_week(self, request):
        """获取本周的日报"""
        today = timezone.now().date()
        # 计算本周的开始（周一）和结束（周日）
        start_date = today - timedelta(days=today.weekday())
        end_date = start_date + timedelta(days=6)

        queryset = self.get_queryset().filter(date__range=[start_date, end_date])
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class WeeklyReportViewSet(viewsets.ModelViewSet):
    """周报视图集"""

    serializer_class = WeeklyReportSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """只返回当前用户的周报"""
        return WeeklyReport.objects.filter(user=self.request.user)

    @action(detail=False, methods=["post"])
    def generate(self, request):
        """生成周报"""
        serializer = WeeklyReportGenerateSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)

        start_date = serializer.validated_data["start_date"]
        end_date = serializer.validated_data["end_date"]
        use_daily_reports = serializer.validated_data.get("use_daily_reports", False)

        # 准备内容
        content = serializer.validated_data.get("content", "")

        # 如果使用日报内容，从日报中提取
        if use_daily_reports:
            daily_reports = DailyReport.objects.filter(user=request.user, date__range=[start_date, end_date]).order_by(
                "date"
            )

            if daily_reports:
                # 合并日报内容
                completed_tasks = []
                planned_tasks = []
                issues = []

                for report in daily_reports:
                    if report.completed_tasks:
                        completed_tasks.append(f"{report.date.strftime('%m-%d')}: {report.completed_tasks}")
                    if report.planned_tasks:
                        planned_tasks.append(f"{report.date.strftime('%m-%d')}: {report.planned_tasks}")
                    if report.issues:
                        issues.append(f"{report.date.strftime('%m-%d')}: {report.issues}")

                content = "本周工作内容:\n" + "\n".join(completed_tasks)
                if planned_tasks:
                    content += "\n\n下周计划:\n" + "\n".join(planned_tasks)
                if issues:
                    content += "\n\n遇到的问题:\n" + "\n".join(issues)

        # 启动异步任务生成周报
        task = generate_weekly_report_task.delay(
            user_id=request.user.id, content=content, start_date=start_date.isoformat(), end_date=end_date.isoformat()
        )

        return Response({"task_id": task.id, "status": "processing", "message": "周报生成请求已提交，正在处理中"})

    @action(detail=False, methods=["get"])
    def task_status(self, request):
        """查询任务状态"""
        task_id = request.query_params.get("task_id")
        if not task_id:
            return Response({"error": "缺少task_id参数"}, status=status.HTTP_400_BAD_REQUEST)

        # 从Celery获取任务状态
        task = generate_weekly_report_task.AsyncResult(task_id)

        if task.state == "PENDING":
            response = {"status": "pending", "message": "任务正在排队中"}
        elif task.state == "STARTED":
            response = {"status": "started", "message": "任务正在处理中"}
        elif task.state == "SUCCESS":
            response = {"status": "success", "result": task.result, "message": "周报生成成功"}
        else:
            response = {"status": "failed", "error": str(task.result), "message": "周报生成失败"}

        return Response(response)

    @action(detail=False, methods=["get"])
    def current(self, request):
        """获取当前周的周报"""
        today = timezone.now().date()
        year = today.isocalendar()[0]
        week_number = today.isocalendar()[1]

        try:
            weekly_report = self.get_queryset().get(year=year, week_number=week_number)
            serializer = self.get_serializer(weekly_report)
            return Response(serializer.data)
        except WeeklyReport.DoesNotExist:
            return Response({"detail": "当前周的周报尚未创建"}, status=status.HTTP_404_NOT_FOUND)
