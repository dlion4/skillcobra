import uuid

from django.shortcuts import redirect
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build


def create_google_meet_event(request):
    credentials_info = request.session.get("google_credentials")
    if not credentials_info:
        return redirect("google_calendar_auth")
    credentials = Credentials(**credentials_info)
    service = build("calendar", "v3", credentials=credentials)
    # Create an event
    event = {
            "summary": "Test Meeting",
            "description": "Google Meet Test Event",
            "start": {"dateTime": "2024-11-18T10:00:00", "timeZone": "UTC"},
            "end": {"dateTime": "2024-11-18T11:00:00", "timeZone": "UTC"},
            "conferenceData": {
                "createRequest": {
                    "requestId": str(uuid.uuid4),
                    "conferenceSolutionKey": {"type": "hangoutsMeet"},
                },
            },
        }

    print(event)

    created_event = (
            service.events()
            .insert(
                calendarId="primary",
                body=event,
                conferenceDataVersion=1,
            )
            .execute()
        )
    return created_event["hangoutLink"]
