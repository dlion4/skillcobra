import uuid
import zoneinfo

from django.shortcuts import redirect
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build

from config.settings.base import BASE_DIR


# Convert datetime to the format needed for Google Calendar (ISO 8601 with timezone)
def convert_to_google_format(dt):
    return dt.astimezone(zoneinfo.ZoneInfo(key="UTC")).strftime(
        "%Y-%m-%dT%H:%M:%S+00:00",
    )


def google_calendar_auth(request):
    flow = Flow.from_client_secrets_file(
        str(BASE_DIR / "credential1.json"),
        scopes=["https://www.googleapis.com/auth/calendar"],
        redirect_uri="https://93ac-41-90-70-133.ngrok-free.app/google-calendar/callback/",
    )
    auth_url, _ = flow.authorization_url(prompt="consent")
    return redirect(auth_url)

def google_calendar_callback(request):
    flow = Flow.from_client_secrets_file(
        str(BASE_DIR / "credential1.json"),
        scopes=["https://www.googleapis.com/auth/calendar"],
        redirect_uri="https://93ac-41-90-70-133.ngrok-free.app/google-calendar/callback/",
    )

    flow.fetch_token(authorization_response=request.build_absolute_uri())
    credentials = flow.credentials

    # Save credentials in session or database for authenticated user
    request.session["google_credentials"] = {
        "token": credentials.token,
        "refresh_token": credentials.refresh_token,
        "token_uri": credentials.token_uri,
        "client_id": credentials.client_id,
        "client_secret": credentials.client_secret,
        "scopes": credentials.scopes,
    }
    return redirect("create_google_meet_event")

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

    created_event = service.events().insert(
        calendarId="primary",
        body=event,
        conferenceDataVersion=1,
    ).execute()
    print(created_event)

    return redirect(created_event["hangoutLink"])
