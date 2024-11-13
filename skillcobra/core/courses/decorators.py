from functools import wraps

from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from skillcobra.school.models import Course


def object_item_available(func):
    @wraps(func)
    def wrapper(request, course_pk, course_slug):
        if not hasattr(request.user, "user_profile"):
            return JsonResponse({"error": "User profile not found"}, status=400)
        course = get_object_or_404(
            Course, pk=course_pk, slug=course_slug,
        )
        request.course = course
        return func(request, course_pk, course_slug)
    return wrapper
