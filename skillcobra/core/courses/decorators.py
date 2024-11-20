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


def verify_student_coupon(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        if not hasattr(request.user, "user_profile"):
            return JsonResponse(
                {"error": "User profile not found for the authenticated user."},
                status=400,
            )
        student = request.user.user_profile
        if not hasattr(request, "coupon"):
            return JsonResponse(
                {"error": "Coupon not provided in the request."}, status=400,
            )
        coupon = request.coupon
        if student.pk in coupon.students.values_list("pk", flat=True):
            return JsonResponse(
                {"error": "Coupon has already been applied by this student."},
                status=400,
            )
        return func(request, *args, **kwargs)
    return wrapper
