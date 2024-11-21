import contextlib
import json
import logging

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.layers import get_channel_layer

from skillcobra.memberships.models import MembershipCardCapture
from skillcobra.users.models import Profile

logger = logging.getLogger(__name__)

channel_layer = get_channel_layer()


class AsyncNotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        logger.info(
            f"User {self.scope['user']} is connecting to WebSocket"
        )  # noqa: G004
        self.course_id = self.scope["url_route"]["kwargs"]["course_pk"]
        self.channel_name = f"course_{self.course_id}"
        await self.channel_layer.group_add(self.channel_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        logger.info(
            f"User {self.scope['user']} is disconnecting from WebSocket",
        )  # noqa: G004
        await self.channel_layer.group_discard(self.channel_name, self.channel_name)

    async def send_notification(self, event):
        logger.info(
            f"Sending notification for {self.course_id}: {event['message']}"
        )  # noqa: G004
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


class AsyncCaptureProfileMembershipCardInformation(AsyncWebsocketConsumer):
    async def connect(self):
        return await super().connect()

    async def disconnect(self, close_code):
        await super().disconnect(close_code)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        await self.save_card_information(text_data_json)
        await self.send(
            text_data=json.dumps(
                {
                    "message": "Card saved for future renewal",
                },
            ),
        )

    @database_sync_to_async
    def save_card_information(self, data):
        profile = Profile.objects.get(user=self.scope["user"])
        with contextlib.suppress(Exception):
            if capture := MembershipCardCapture.objects.filter(
                profile=profile,
                card_number=data["account_number"],
            ).first():
                update_fields = ["exp_month", "exp_year", "cvv", "card_holder_name"]
                for field in update_fields:
                    setattr(capture, field, data[field])
                capture.save()
            else:
                capture = MembershipCardCapture.objects.create(
                    profile=profile,
                    card_number=data["account_number"],
                    card_holder_name=data["account_name"],
                    card_cvv_number=data["cvv"],
                    expiry_month=data["exp_month"],
                    expiry_year=data["exp_year"],
                )


class AsyncTerminalWebConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = "terminal_room"
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        await self.channel_layer.group_send(
            self.room_group_name, {"type": "terminal_message", "message": message}
        )

    async def terminal_message(self, event):
        message = event["message"]
        await self.send(text_data=json.dumps({"message": message}))


# class AsyncMonacoCodeEditorWebConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         self.room_group_name = "monaco_code_editor"
#         await self.channel_layer.group_add(self.room_group_name, self.channel_name)
#     async def disconnect(self, code):
#         await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
#     async def receive(self, text_data):
#         text_data_json = json.loads(text_data)
#         code = text_data_json["code"]
#         await self.channel_layer.group_send(
#             self.room_group_name, {"type": "monaco_editor_code", "code": code},
#         )
#     async def monaco_editor_code(self, event):
#         code = event["code"]
#         await self.send(text_data=json.dumps({"code": code}))


class AsyncMonacoCodeEditorWebConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.room_group_name = "code_editor_room"
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        logger.info(f"User {self.scope['user']} connected to Monaco Code Editor")  # noqa: G004
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
        logger.info(f"User {self.scope['user']} disconnected from Monaco Code Editor")  # noqa: G004
        await super().disconnect(close_code)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        user = text_data_json["user"]
        code = text_data_json["code"]
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "send_editor_message",
                "user": user,
                "code": code,
            },
        )

    async def send_editor_message(self, event):
        user = event["user"]
        code = event["code"]
        # Send message to WebSocket
        print(code)
        await self.send(
            text_data=json.dumps(
                {
                    "user": user,
                    "code": code,
                },
            ),
        )
