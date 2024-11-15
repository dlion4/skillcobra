import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from skillcobra.core.forms import MessageForm
from skillcobra.core.models import Message as MessageModel
from skillcobra.core.serializers import MessageSerializer
from skillcobra.users.models import Profile


class AsyncMessageTutorConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.student = self.scope["user"]
        self.tutor_pk = self.scope["url_route"]["kwargs"]["tutor_pk"]
        self.room_name = f"tutor_{self.tutor_pk}"
        self.room_group_name = f"message_{self.room_name}"
        self.message_form_class = await self.get_message_form_class()
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
        await super().disconnect(code)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        form = await self.create_message_form(message)
        if form.is_valid():
            saved_message = await self.save_message(form)
            await self.send_message_to_group(saved_message)
        else:
            return

    async def send_message_to_group(self, message):
        count = await self.get_message_count(self.tutor_pk)  # Get
        await self.channel_layer.group_send(
            self.room_group_name,
            {"type": "chat_message", "message": message, "count": count},
        )

    async def chat_message(self, event):
        message = event["message"]
        count = event["count"]
        await self.send(text_data=json.dumps({"message": message, "count": count}))


    @database_sync_to_async
    def get_message_form_class(self):
        return lambda data: MessageForm(data=data, profile=self.student.user_profile)

    @database_sync_to_async
    def create_message_form(self, message):
        return self.message_form_class(message)

    @database_sync_to_async
    def save_message(self, form):
        message = form.save(commit=False)
        message.sender = self.student.user_profile
        message.receiver = self.get_tutor_profile()
        message.save()
        serializer = MessageSerializer(instance=message)
        message.delete()
        return serializer.data

    def get_tutor_profile(self):
        return Profile.objects.get(pk=self.tutor_pk)

    @database_sync_to_async
    def get_message_count(self, tutor_pk):
        # Implement logic to get the current count of messages for this tutor
        # This could be based on your application's logic (e.g., counting unread messages)
        return MessageModel.objects.filter(
            receiver__pk=tutor_pk,
            is_read=False,
        ).count()
