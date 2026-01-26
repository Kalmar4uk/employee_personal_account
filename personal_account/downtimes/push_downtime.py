import json

import redis
from django.conf import settings

from downtimes.models import Downtime
from utils.constants import NAME_CHANNEL_REDIS

try:
    redis_connect = redis.Redis.from_url(settings.REDIS_URL)
except Exception:
    settings.HAWK.send()


def created_send_downtime(downtine: Downtime):
    try:
        message = {
            "event": "created_new_downtime",
            "service": downtine.service,
            "start_downtime": downtine.start_downtime.isoformat(),
            "end_downtime": downtine.end_downtime.isoformat(),
            "gsma_employee": (
                f"{downtine.gsma_employee.last_name} "
                f"{downtine.gsma_employee.first_name}"
            ),
            "link": downtine.link_task,
            "description": downtine.description,
            "first_reminder": (
                downtine.reminder_downtime.first_reminder.isoformat()
            ),
            "second_reminder": (
                downtine.reminder_downtime.second_reminder.isoformat()
            )
        }

        message_pub = redis_connect.publish(
            NAME_CHANNEL_REDIS, json.dumps(message)
        )
        if message_pub:
            downtine.reminder_downtime.success_reminder = True
            downtine.save()
    except Exception:
        settings.HAWK.send()
