import json
import logging

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.layers import get_channel_layer

logger = logging.getLogger(__name__)

channel_layer = get_channel_layer()

class AsyncNotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        logger.info(f"User {self.scope['user']} is connecting to WebSocket")  # noqa: G004
        self.course_id = self.scope["url_route"]["kwargs"]["course_pk"]
        self.channel_name = f"course_{self.course_id}"
        await self.channel_layer.group_add(self.channel_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        logger.info(f"User {self.scope['user']} is disconnecting from WebSocket")  # noqa: G004
        await self.channel_layer.group_discard(self.channel_name, self.channel_name)

    async def send_notification(self, event):
        logger.info(f"Sending notification for {self.course_id}: {event['message']}")  # noqa: G004
        message = event["message"]
        await self.send(text_data=json.dumps({"message": message}))
    async def broadcast_notification(self, message):
        await self.channel_layer.group_send(
            self.channel_name,
            {
                "type": "send_notification",
                "message": message,
            },
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        logger.info(f"Received message: {data}")  # noqa: G004
        if data["type"] == "like_action":
            await self.broadcast_notification({"message": data["message"]})
