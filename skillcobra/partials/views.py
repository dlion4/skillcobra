from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from roles.students.students.models import Attendance
from skillcobra.school.models import Course
from skillcobra.users.models import Profile


@login_required
@csrf_exempt
def get_attendance_data(request):
    query = request.GET.get("q", "").strip()
    profile = request.user.user_profile
    if query == "0":
        courses = Course.objects.filter(tutor=profile)
    else:
        try:
            query_year = int(query)
            courses = Course.objects.filter(created_at__year=query_year, tutor=profile)
        except ValueError:
            courses = Course.objects.none()  # No courses if query is invalid
    template_name = "instructors/partials/attendance/filter.html"
    return render(request, template_name, {"courses": courses})
