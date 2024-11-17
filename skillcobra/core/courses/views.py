import time

from channels.layers import get_channel_layer
from django.contrib.auth import get_user
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.views.generic import DetailView

from roles.instructors.instructor.models import ScheduleClass
from skillcobra.core.courses.decorators import object_item_available
from skillcobra.purchases.models import Cart
from skillcobra.school.models import Course

channel_layer = get_channel_layer()


class CourseDetailView(DetailView):
    model = Course
    template_name = "pages/course_detail.html"
    context_object_name = "course"

    def get_object(self, queryset=None):
        return get_object_or_404(
            self.model,
            pk=self.kwargs.get("pk"),
            slug=self.kwargs.get("slug"),
        )

    def get_profile(self):
        return get_user(self.request).user_profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_course_items = (
            self.get_profile().get_all_cart_items().values_list("pk", flat=True)
        )
        purchased_courses = self.get_profile().purchased_courses.values_list(
            "pk", flat=True,
        )
        context["cart_course_items"] = cart_course_items
        context["purchased_courses"] = purchased_courses
        return context

    def get(self, request, *args, **kwargs):
        course = self.get_object()
        request.session["course_item_id"] = course.pk
        return super().get(request, *args, **kwargs)


@login_required
@csrf_exempt
@object_item_available
@require_POST
def course_handle_like_click_view(request, course_pk, course_slug):
    course = request.course
    user = request.user
    if request.session.get("course_id"):
        return JsonResponse(
            {"status": "Already", "views": str(course.views)},
            status=200,
        )
    request.session["course_id"] = course.pk
    course.views += 1
    course.save()
    return JsonResponse(
        {
            "type": "like_action",
            "course_title": str(course.title),
            "status": "Liked",
            "views": str(course.views),
            "user": str(user.user_profile.full_name()),
        },
        status=200,
    )


@login_required
@csrf_exempt
@object_item_available
@require_POST
def course_handle_unlike_click_view(request, course_pk, course_slug):
    course = request.course
    if request.session.get("course_id", None):
        del request.session["course_id"]
        course.views -= 1
        course.save()
        return JsonResponse({"views": str(course.views)}, status=200)
    return JsonResponse({"views": str(course.views)}, status=200)


@login_required
@csrf_exempt
@object_item_available
@require_POST
def add_course_to_cart_view(request, course_pk, course_slug):
    profile_cart, _ = Cart.objects.get_or_create(student=request.user.user_profile)
    if request.course.pk not in profile_cart.courses.values_list("pk", flat=True):
        profile_cart.courses.add(request.course)
        profile_cart.total_price += request.course.payable_amount
        profile_cart.save()
    return JsonResponse(
        {"cart_count": str(profile_cart.courses.all().count())},
        status=201,
    )


@login_required
@csrf_exempt
@object_item_available
@require_POST
def remove_course_from_cart(request, course_pk, course_slug):
    profile_cart, _ = Cart.objects.get_or_create(student=request.user.user_profile)
    if request.course.pk in profile_cart.courses.values_list("pk", flat=True):
        profile_cart.courses.remove(request.course)
        profile_cart.total_price -= request.course.payable_amount
        profile_cart.save()
    return JsonResponse(
        {"cart_count": str(profile_cart.courses.all().count())},
        status=200,
    )


@login_required
@csrf_exempt
def live_class_short_url_redirect(request, short_url):
    schedule_class = get_object_or_404(ScheduleClass, short_url=short_url)
    return redirect(schedule_class.class_live_link)
