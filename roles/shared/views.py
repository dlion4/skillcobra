import uuid
import zoneinfo

from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views import View
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from django.contrib import messages
from config.settings.base import BASE_DIR
from roles.instructors.instructor.forms import ScheduleClassForm


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
    return redirect("")


def create_google_meet_event(request):
    credentials_info = request.session.get("google_credentials")
    if not credentials_info:
        return redirect("google_calendar_auth")
    credentials = Credentials(**credentials_info)
    service = build("calendar", "v3", credentials=credentials)
    class_data = request.session.get("form_data_class_link")
    start_time = class_data["class_start_time"].isoformat()
    end_time = class_data["class_end_time"].isoformat()
    event_summary = class_data.get("title", "Scheduled Class")
    event_description = class_data.get("lesson_overview", "Class Description")
    event = {
        "summary": event_summary,
        "description": event_description,
        "start": {"dateTime": start_time, "timeZone": "UTC"},
        "end": {"dateTime": end_time, "timeZone": "UTC"},
        "conferenceData": {
            "createRequest": {
                "requestId": str(uuid.uuid4()),
                "conferenceSolutionKey": {"type": "hangoutsMeet"},
            },
        },
    }

    created_event = (
        service.events()
        .insert(
            calendarId="primary",
            body=event,
            conferenceDataVersion=1,
        )
        .execute()
    )

    response_data = {
        "detail": "Class scheduled successfully.",
        "google_meet_link": created_event["hangoutLink"],
    }
    form = ScheduleClassForm(
        data=class_data,
        profile=request.user.user_profile,
    )
    if form.is_valid():
        messages.success(request, "Link created successfully")
        return _handle_create_google_meet_event(
            form,
            created_event,
            response_data,
        )
    messages.error(request, "Failed to create the link")
    return redirect(created_event["hangoutLink"])


def _handle_create_google_meet_event(form, created_event, response_data):
    instance = form.save()
    instance.class_live_link = created_event["hangoutLink"]
    instance.save()
    form.save()
    response_data["course_id"] = instance.courses.pk
    return redirect(reverse("instructors:dashboard"))


class CreateGoogleMeetEventView(View):
    fallback_url = reverse_lazy("instructors:streaming_setup")

    def get(self, request, *args, **kwargs):
        # Fetch Google credentials from session
        credentials_info = request.session.get("google_credentials")
        if not credentials_info:
            return redirect("google_calendar_auth")

        # Build Google API service
        credentials = Credentials(**credentials_info)
        service = build("calendar", "v3", credentials=credentials)

        # Fetch class data from session
        class_data = request.session.get("form_data_class_link")
        if not class_data:
            messages.error(
                request, "something went wrong on our endpoint! Please try again.",
            )
            return redirect(self.fallback_url)  # Redirect if no session data

        # Extract event details
        start_time = class_data["class_start_time"].isoformat()
        end_time = class_data["class_end_time"].isoformat()
        event_summary = class_data.get("title", "Scheduled Class")
        event_description = class_data.get("lesson_overview", "Class Description")

        # Create Google Calendar event
        event = {
            "summary": event_summary,
            "description": event_description,
            "start": {"dateTime": start_time, "timeZone": "UTC"},
            "end": {"dateTime": end_time, "timeZone": "UTC"},
            "conferenceData": {
                "createRequest": {
                    "requestId": str(uuid.uuid4()),
                    "conferenceSolutionKey": {"type": "hangoutsMeet"},
                },
            },
        }

        try:
            created_event = (
                service.events()
                .insert(
                    calendarId="primary",
                    body=event,
                    conferenceDataVersion=1,
                )
                .execute()
            )
        except Exception as e:
            messages.error(request, f"Failed to create Google Meet event: {e}")
            return redirect(self.fallback_url)
        # Prepare response data
        response_data = {
            "detail": "Class scheduled successfully.",
            "google_meet_link": created_event["hangoutLink"],
        }

        # Validate and save form
        form = ScheduleClassForm(
            data=class_data,
            profile=request.user.user_profile,
        )
        if form.is_valid():
            return self._handle_create_google_meet_event(
                request,
                form,
                created_event,
                response_data,
            )
        messages.error(request, "Failed to create the link")
        return redirect(self.fallback_url)

    def _handle_create_google_meet_event(
        self,
        request,
        form,
        created_event,
        response_data,
    ):
        instance = form.save()
        instance.class_live_link = created_event["hangoutLink"]
        instance.save()
        form.save()
        response_data["course_id"] = instance.courses.pk
        messages.success(request, "successfully created class link")
        return redirect("instructors:dashboard")
