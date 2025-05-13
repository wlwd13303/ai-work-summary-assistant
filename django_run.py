import os
import sys


def main():
    '''Run Django development server'''
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_app.config.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed? "
        ) from exc

    execute_from_command_line(['manage.py', 'runserver', '0.0.0.0:8001'])


if __name__ == '__main__':
    main()
