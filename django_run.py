import os
import sys
from pathlib import Path


def main():
    """Run Django development server"""
    # 添加django_app目录到Python路径
    current_path = Path(__file__).parent.absolute()
    django_app_path = os.path.join(current_path, "django_app")
    sys.path.append(str(django_app_path))

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError("Couldn't import Django. Are you sure it's installed?") from exc
    execute_from_command_line(["manage.py", "runserver", "0.0.0.0:8001"])


if __name__ == "__main__":
    main()
