# my_project/celery.py

from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings

# Django의 기본 설정을 Celery에 연결
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

app = Celery("friend")
# app.conf.enable_utc = False

# Django의 설정 파일에서 Celery 관련 설정을 가져오기
app.config_from_object("django.conf:settings", namespace="CELERY")

# Django에 등록된 앱에서 task 모듈을 자동으로 찾도록 설정
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
app.conf.timezone = "Asia/Seoul"

from notifications.task import get_infos, gather_infos, create_notifications_task
