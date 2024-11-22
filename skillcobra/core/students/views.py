from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from skillcobra.core.forms import EnrollmentForm
from skillcobra.core.models import Enrollment
from skillcobra.core.students.mixins import LikeCourseViewMixin
from skillcobra.core.students.mixins import UnLikeCourseViewMixin
from skillcobra.school.models import SavedCourse


class SaveCourseView(LikeCourseViewMixin, View):
    def post(self, request, *args, **kwargs):
        course = request.course
        return JsonResponse({"status": "success", "message": f"Course {course.title} liked"})  # noqa: E501


class RemoveSavedCourseView(UnLikeCourseViewMixin, View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    def post(self, request, *args, **kwargs):
        return JsonResponse({}, status=204)

class RemoveAllSavedCoursesView(LoginRequiredMixin, View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        saved_courses = SavedCourse.objects.get(student=request.user.user_profile)
        saved_courses.delete()
        return JsonResponse({}, status=204)

class RegisterEnrollmentView(LoginRequiredMixin, View):
    form_class = EnrollmentForm
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, profile=request.user.user_profile)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.profile = request.user.user_profile
            instance.save()
            form.save()
            return JsonResponse({"is_enrolled": True}, status=204)
        return JsonResponse({"is_enrolled": False}, status=400)

class CheckEnrollmentStatusView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        is_enrolled = Enrollment.objects.filter(profile=request.user.user_profile)
        return JsonResponse({"is_enrolled": is_enrolled.exists()})
