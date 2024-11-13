import threading
import time

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from .thread import MainThreadPool


class NotificationService:
    def __init__(self, workers=5, *args, **kwargs):
        self.thread_pool = MainThreadPool(max_workers=workers)
        self.channel_layer = get_channel_layer()

    def _send_notification(self, user, message):
        async_to_sync(
            self.channel_layer.group_send(
                f"user_{user.pk}",
                {
                    "type": "send_notification",
                    "message": message,
                    "timestamp": int(time.time()),
                },
            ),
        )
    def send_like_notification(self, user, data):
        print("hello user", user)
        self.thread_pool.submit(self._send_notification, user=user, message=data)
        print("hello data", data)
        self.thread_pool.task_queue.join()
        self.thread_pool.shutdown()
