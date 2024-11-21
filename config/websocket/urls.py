from django.urls import path

from skillcobra.core.instructors.consumer import AsyncMessageTutorConsumer

from .consumer import AsyncCaptureProfileMembershipCardInformation
from .consumer import AsyncMonacoCodeEditorWebConsumer
from .consumer import AsyncNotificationConsumer
from .consumer import AsyncTerminalWebConsumer

websocket_urlpatterns = [
    # path("ws/notifications/", AsyncNotificationConsumer.as_asgi()),
    path("ws/notifications/<course_pk>", AsyncNotificationConsumer.as_asgi()),
    path("ws/message/<tutor_pk>", AsyncMessageTutorConsumer.as_asgi()),
    path(
        "ws/membership/completed/checkout",
        AsyncCaptureProfileMembershipCardInformation.as_asgi(),
    ),
    path(
        "ws/editor/sessions/ide",
        AsyncTerminalWebConsumer.as_asgi(),
    ),
    path(
        "ws/editor/sessions/ide/code",
        AsyncMonacoCodeEditorWebConsumer.as_asgi(),
    ),
]
