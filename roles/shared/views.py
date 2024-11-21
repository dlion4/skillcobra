import json
import os
import subprocess
import tempfile
import uuid
import zoneinfo

from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.urls import reverse_lazy
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build

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
class WebEditorView(TemplateView):
    template_name = "core/editor.html"


@csrf_exempt
def execute_code(request):
    if request.method != "POST":
        return JsonResponse({"output": "Invalid request method."}, status=405)
    try:
        data = json.loads(request.body)
        code = data.get("code")
        language = data.get("language")
        # Define interpreters for supported languages
        interpreters = {
            "python": ["python3", "-c"],
            "javascript": ["node", "-e"],
            "typescript": ["ts-node", "-e"],
            "go": ["go", "run"],
            "rust": ["cargo", "run"],
        }

        if language not in interpreters:
            return JsonResponse(
                {"output": f"Language '{language}' is not supported."}, status=400,
            )

        # Prepare the subprocess call
        interpreter = interpreters[language]
        process = subprocess.Popen(
            [*interpreter, code],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        stdout, stderr = process.communicate()
        if process.returncode == 0:
            return JsonResponse({"output": stdout})
        return JsonResponse({"output": stderr}, status=400)
    except Exception as e:
        print(e)
        return JsonResponse({"output": str(e)}, status=500)


def save_code_to_temp_file(code, extension):
    temp_dir = tempfile.gettempdir()
    file_path = os.path.join(temp_dir, f"temp_code.{extension}")
    with open(file_path, "w") as f:
        f.write(code)
    return file_path


def run_typescript_code(file_path):
    # First, compile TypeScript to JavaScript
    compile_process = subprocess.run(["tsc", file_path], capture_output=True, text=True)  # noqa: S607
    if compile_process.returncode != 0:
        return compile_process.stderr

    # Then, run the compiled JavaScript code
    js_file = file_path.replace(".ts", ".js")
    run_process = subprocess.run(["node", js_file], capture_output=True, text=True)
    return run_process.stdout if run_process.returncode == 0 else run_process.stderr


def run_go_code(file_path):
    # Run the Go file directly
    run_process = subprocess.run(
        ["go", "run", file_path], capture_output=True, text=True
    )
    return run_process.stdout if run_process.returncode == 0 else run_process.stderr


def run_rust_code(file_path):
    # Compile the Rust code
    compile_process = subprocess.run(
        ["rustc", file_path], capture_output=True, text=True,
    )
    if compile_process.returncode != 0:
        return compile_process.stderr

    # Run the compiled Rust executable
    executable_file = file_path.replace(".rs", "")
    run_process = subprocess.run([executable_file], capture_output=True, text=True)
    return run_process.stdout if run_process.returncode == 0 else run_process.stderr


def run_javascript_code(code):
    # Run the JavaScript code via Node.js
    temp_file = save_code_to_temp_file(code, "js")
    run_process = subprocess.run(["node", temp_file], capture_output=True, text=True)
    return run_process.stdout if run_process.returncode == 0 else run_process.stderr
