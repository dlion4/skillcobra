from datetime import timedelta

from django.contrib.auth import get_user
from django.db import IntegrityError
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import FormView
from django.views.generic import TemplateView

from skillcobra.school.forms import CourseCurriculumForm
from skillcobra.school.forms import CourseForm
from skillcobra.school.forms import CreateCourseCurriculumLectureForm
from skillcobra.school.models import Course
from skillcobra.users.forms import UpdateAccountProfileBasicDataForm


class TemplateViewMixin(TemplateView):
    template_name = ""

    def get_template_names(self):
        return [f"instructors/{self.template_name}"]
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        if (
            request.user.is_authenticated
            and request.user.role == "instructor"
            and not request.path.startswith("/instructor")
        ):
            return redirect("instructors:dashboard")
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
        error_messages:list[str] = []
        for field, errors in form.errors.items():
            error_messages.extend(
                {"field": field, "message": error} for error in errors)
        return JsonResponse({"errors": error_messages}, status=400)

class InstructorProfileUpdateView(TemplateViewMixin):
    template_name = "profile_update.html"
    account_basic_form = UpdateAccountProfileBasicDataForm
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["account_basic_update_form"] = self.account_basic_form(
            instance=self.get_profile(),
        )
        return context

class InstructorAnalyticsView(TemplateViewMixin):
    template_name = "analytics.html"
