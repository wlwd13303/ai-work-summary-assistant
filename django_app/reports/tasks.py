from celery import shared_task
import requests
import json
import logging
from django.conf import settings
from django.contrib.auth import get_user_model
from datetime import datetime
from .models import WeeklyReport

logger = logging.getLogger(__name__)
User = get_user_model()


@shared_task
def generate_weekly_report_task(user_id, content, start_date, end_date):
    """异步生成周报任务"""
    try:
        # 获取用户
        user = User.objects.get(id=user_id)

        # 解析日期
        start_date_obj = datetime.fromisoformat(start_date).date()
        end_date_obj = datetime.fromisoformat(end_date).date()

        # 调用FastAPI服务生成周报
        fastapi_url = f"{settings.FASTAPI_URL}/api/v1/text-generation/generate_report"

        payload = {
            "content": content
        }

        headers = {
            "Content-Type": "application/json"
        }

        response = requests.post(fastapi_url, data=json.dumps(payload), headers=headers)

        if response.status_code == 200:
            result = response.json()
            generated_text = result.get("generated_text", "")

            # 计算年份和周数
            year = start_date_obj.isocalendar()[0]
            week_number = start_date_obj.isocalendar()[1]

            # 创建或更新周报
            weekly_report, created = WeeklyReport.objects.update_or_create(
                user=user,
                year=year,
                week_number=week_number,
                defaults={
                    'start_date': start_date_obj,
                    'end_date': end_date_obj,
                    'content': generated_text,
                    # 以下字段可以根据生成的文本进行解析填充，这里简单处理
                    'achievements': '',
                    'plans': '',
                    'issues': '',
                    'thoughts': ''
                }
            )

            return {
                'weekly_report_id': weekly_report.id,
                'generated_text': generated_text
            }
        else:
            logger.error(f"FastAPI服务返回错误: {response.status_code}, {response.text}")
            raise Exception(f"FastAPI服务返回错误: {response.status_code}")

    except Exception as e:
        logger.error(f"生成周报失败: {str(e)}")
        raise e