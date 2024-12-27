import uuid
from datetime import timedelta

from django.contrib.auth import get_user
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import IntegrityError
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import FormView
from django.views.generic import TemplateView
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

from roles.instructors.instructor.forms import ScheduleClassForm
from roles.instructors.instructor.models import ScheduleClass
from skillcobra.payments.forms import BillingAddressForm
from skillcobra.school.forms import CourseCurriculumForm
from skillcobra.school.forms import CourseForm
from skillcobra.school.forms import CreateCourseCurriculumLectureForm
from skillcobra.school.models import Course
from skillcobra.users.forms import UpdateAccountProfileBasicDataForm


class TemplateViewMixin(LoginRequiredMixin, TemplateView):
    template_name = ""
    login_url = "/users/login/"

    def get_template_names(self):
        return [f"instructors/{self.template_name}"]

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        if request.user.role != "instructor":
            return redirect("home")
        return super().dispatch(request, *args, **kwargs)

    def get_profile(self):
        return get_user(self.request).user_profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["profile"] = self.get_profile()
        return context


# Create your views here.
class InstructorDashboardView(TemplateViewMixin):
    template_name = "dashboard.html"

    def get_courses(self):
        return Course.objects.filter(tutor=self.get_profile())

    def get_new_courses(self):
        # Get the current time
        now = timezone.now()
        # Filter courses that were created in the last 3 days
        three_days_ago = now - timedelta(days=3)
        return Course.objects.filter(
            tutor=self.get_profile(),
            created_at__gte=three_days_ago,
        ).prefetch_related("sub_category")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["courses"] = self.get_courses()
        context["new_courses"] = self.get_courses()
        return context


class InstructorCoursesView(TemplateViewMixin):
    template_name = "courses.html"


class InstructorCreatedCourseView(TemplateViewMixin, FormView):
    template_name = "create_course.html"
    form_class = CourseForm

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.tutor = self.get_profile()
            instance.save()
            form.save()
            return redirect(instance)
        context = {"form": form}
        return render(request, self.get_template_names(), context)


class InstructorCourseDetailView(TemplateViewMixin, FormView):

    template_name = "course_detail.html"
    form_class = CourseCurriculumForm
    lecture_form = CreateCourseCurriculumLectureForm

    def get_course_item(self):
        return get_object_or_404(
            Course,
            tutor=self.get_profile(),
            pk=self.kwargs.get("pk"),
            slug=self.kwargs.get("slug"),
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["course"] = self.get_course_item()
        context["lecture_form"] = self.lecture_form()
        return context

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            try:
                instance = form.save(commit=False)
                instance.course = self.get_course_item()
                instance.tutor = self.get_profile()
                instance.save()
                return JsonResponse({"message": "Successfully created."}, status=201)
            except IntegrityError:
                return JsonResponse(
                    {
                        "errors": "Duplicate module title error!",
                    },
                    status=500,
                )
        error_messages: list[str] = []
        for field, errors in form.errors.items():
            error_messages.extend(
                {"field": field, "message": error} for error in errors
            )
        return JsonResponse({"errors": error_messages}, status=400)


class InstructorProfileUpdateView(TemplateViewMixin):
    template_name = "profile_update.html"
    account_basic_form = UpdateAccountProfileBasicDataForm
    billing_form = BillingAddressForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["account_basic_update_form"] = self.account_basic_form(
            instance=self.get_profile(),
        )
        context["billing_form"] = self.billing_form(profile=self.get_profile())
        return context


class InstructorAnalyticsView(TemplateViewMixin):
    template_name = "analytics.html"


class InstructorStreamingView(TemplateViewMixin):
    template_name = "stream.html"


class InstructorEarningView(TemplateViewMixin):
    template_name = "earnings.html"


class InstructorPayoutView(TemplateViewMixin):
    template_name = "payout.html"


class InstructorPaymentStatementView(TemplateViewMixin):
    template_name = "statements.html"


class InstructorStreamSessionView(TemplateViewMixin):
    template_name = "live.html"
    model = ScheduleClass

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["stream_session"] = self.model.objects.filter(
            courses__tutor=self.get_profile(),
        ).distinct()
        return context


class InstructorStreamingSetupView(TemplateViewMixin, FormView):
    template_name = "streaming_setup.html"
    form_class = ScheduleClassForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = self.form_class(profile=self.request.user.user_profile)
        return context

    def post(self, request, *args, **kwargs):
        if "form_data_class_link" not in request.session:
            request.session["form_data_class_link"] = request.POST.dict()
        form = self.form_class(
            data=request.session.get("form_data_class_link"),
            profile=request.user.user_profile,
        )
        credentials_info = request.session.get("google_credentials")
        if not credentials_info:
            return JsonResponse(
                {
                    "url": str(reverse("google_calendar_auth")),
                    "detail": """
                    Failed, but you'll be redirected to Google.
                    Use your registered email to auto-generate the class link,
                    when redirected to google page""",
                },
                status=403,
            )
        if form.is_valid():
            class_data = form.cleaned_data
            try:
                return self._handle_google_meet_session_creation(
                    request,
                    class_data,
                    form,
                    credentials_info,
                )
            except Exception as e:  # noqa: BLE001
                return JsonResponse(
                    {"detail": f"Failed to create Google Meet event. {e!s}"},
                    status=400,
                )
        del request.session["form_data_class_link"]
        return JsonResponse({"detail": "Invalid form data."}, status=400)

    def _handle_google_meet_session_creation(self, request, class_data, form, creds):
        google_meet_link = self.create_google_meet_event(request, class_data, creds)
        response_data = {
            "detail": "Class scheduled successfully.",
            "google_meet_link": google_meet_link,
        }
        instance = form.save()
        instance.class_live_link = google_meet_link
        instance.save()
        form.save()
        response_data["course_id"] = instance.courses.pk
        return JsonResponse(response_data, status=200)

    def create_google_meet_event(self, request, class_data, creds):
        """
        Creates a Google Meet event and returns the Meet link.
        """

        credentials = Credentials(**creds)
        service = build("calendar", "v3", credentials=credentials)

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
        return created_event.get("hangoutLink")


class InstructorCourseAttendanceView(TemplateViewMixin):
    template_name = "attendance.html"


class InstructorRecruitmentView(TemplateViewMixin):
    template_name = "tutor_recruitment.html"
    def post(self, request, *args, **kwargs):
        return JsonResponse({}, status=200)
