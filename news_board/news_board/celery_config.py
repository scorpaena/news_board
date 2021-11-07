from __future__ import absolute_import, unicode_literals
import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "news_board.settings")

app = Celery("news_board")

app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

app.conf.timezone = "Europe/Kiev"

app.conf.beat_schedule = {
    "reset_post_upvotes": {
        "task": "posts.tasks.reset_post_upvotes",
        "schedule": crontab(minute="0", hour="0"),
    },
}
