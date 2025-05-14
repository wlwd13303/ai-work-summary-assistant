import os
import sys
from pathlib import Path


def main():
    """Run Celery worker"""
    # 添加django_app目录到Python路径
    current_path = Path(__file__).parent.absolute()
    django_app_path = os.path.join(current_path, 'django_app')
    sys.path.append(str(django_app_path))

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

    from celery.__main__ import main as celery_main

    sys.argv = ['celery', 'worker', '--loglevel=info']
    celery_main()


if __name__ == '__main__':
    main()