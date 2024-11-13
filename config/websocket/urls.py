from django.urls import path

from .consumer import AsyncNotificationConsumer

websocket_urlpatterns = [
    # path("ws/notifications/", AsyncNotificationConsumer.as_asgi()),
    path("ws/notifications/<course_pk>", AsyncNotificationConsumer.as_asgi()),
]
