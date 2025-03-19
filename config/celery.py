from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings


# Установка переменной окружения для настроек проекта
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Создание экземпляра объекта Celery
app = Celery('config')

# Загрузка настроек из файла Django
app.config_from_object('django.conf:settings', namespace='CELERY')

# Автоматическое обнаружение и регистрация задач из файлов tasks.py в приложениях Django
app.autodiscover_tasks()

@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    from config.celery_beat_schedule import BEAT_SCHEDULE
    sender.conf.beat_schedule = BEAT_SCHEDULE