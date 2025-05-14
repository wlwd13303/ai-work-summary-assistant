from rest_framework import serializers
from .models import DailyReport, WeeklyReport
from django.utils import timezone
from datetime import datetime, timedelta


class DailyReportSerializer(serializers.ModelSerializer):
    """日报序列化器"""

    class Meta:
        model = DailyReport
        fields = ['id', 'date', 'completed_tasks', 'planned_tasks', 'issues', 'notes', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

    def create(self, validated_data):
        # 自动关联当前用户
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class WeeklyReportSerializer(serializers.ModelSerializer):
    """周报序列化器"""

    class Meta:
        model = WeeklyReport
        fields = ['id', 'year', 'week_number', 'start_date', 'end_date', 'content',
                  'achievements', 'plans', 'issues', 'thoughts', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

    def create(self, validated_data):
        # 自动关联当前用户
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class WeeklyReportGenerateSerializer(serializers.Serializer):
    """周报生成请求序列化器"""
    content = serializers.CharField(required=False, help_text="手动输入的工作内容要点")
    start_date = serializers.DateField(required=False, help_text="周开始日期")
    end_date = serializers.DateField(required=False, help_text="周结束日期")
    use_daily_reports = serializers.BooleanField(default=False, help_text="是否使用日报内容")

    def validate(self, attrs):
        """验证日期范围"""
        # 如果没有提供日期，默认为本周
        if 'start_date' not in attrs or 'end_date' not in attrs:
            today = timezone.now().date()
            # 计算本周的开始（周一）和结束（周日）
            start_date = today - timedelta(days=today.weekday())
            end_date = start_date + timedelta(days=6)
            attrs['start_date'] = start_date
            attrs['end_date'] = end_date

        # 确保开始日期不晚于结束日期
        if attrs['start_date'] > attrs['end_date']:
            raise serializers.ValidationError("开始日期不能晚于结束日期")

        # 如果使用日报内容但没有提供内容，需要验证是否有日报
        if attrs.get('use_daily_reports', False) and 'content' not in attrs:
            user = self.context['request'].user
            daily_reports = DailyReport.objects.filter(
                user=user,
                date__range=[attrs['start_date'], attrs['end_date']]
            )
            if not daily_reports.exists():
                raise serializers.ValidationError("所选日期范围内没有日报记录")

        return attrs