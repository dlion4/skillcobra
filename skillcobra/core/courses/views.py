import time
from decimal import ROUND_HALF_UP
from decimal import Decimal

from channels.layers import get_channel_layer
from django.contrib.auth import get_user
from django.contrib.auth.decorators import login_required
from django.core.exceptions import FieldError
from django.db import DatabaseError
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render
from django.template.exceptions import TemplateDoesNotExist
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.views.generic import DetailView

from roles.instructors.instructor.models import ScheduleClass
from skillcobra.core.courses.decorators import object_item_available
from skillcobra.core.courses.decorators import verify_student_coupon
from skillcobra.filters.index import CourseFilter
from skillcobra.purchases.models import Cart
from skillcobra.purchases.models import Coupon
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
            "pk",
            flat=True,
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
def live_class_short_url_redirect(
    request,
    course_pk,
    course_slug,
    schedule_pk,
    short_url,
):
    schedule_class = get_object_or_404(
        ScheduleClass,
        courses__pk=course_pk,
        courses__slug=course_slug,
        pk=schedule_pk,
        short_url=short_url,
    )
    return redirect(schedule_class.class_live_link)


@login_required
@csrf_exempt
def courses_live_search_view(request):
    template_name = "searches/explore/courses.html"
    try:
        result = Course.objects.filter(
            title__icontains=request.GET.get("search_query", "")
        )
        return render(request, template_name, {"courses": result})
    except (FieldError, TemplateDoesNotExist, Exception, DatabaseError) as e:
        return HttpResponse(f"Error: {e!s}", status=500)


@login_required
@csrf_exempt
def apply_coupon_code_to_cart_item_view(request, *args, **kwargs):
    code = request.POST.get("coupon_code")
    if not code:
        return JsonResponse({"message": "Coupon code is required."}, status=400)
    try:
        profile_cart = Cart.objects.get(student=request.user.user_profile)
    except Cart.DoesNotExist:
        return JsonResponse({"message": "Cart not found for the student."}, status=404)
    coupon_object = Coupon.objects.filter(code=code).first()
    if not coupon_object:
        return JsonResponse({"message": "Invalid coupon code."}, status=404)
    student = request.user.user_profile
    course_with_code = coupon_object.course
    if student in coupon_object.students.all() and coupon_object.is_valid_for_course(
        course_with_code,
    ):
        return JsonResponse(
            {
                "message": "You've already used this coupon code",
                "newPrice": profile_cart.total_price.quantize(
                    Decimal("0.01"),
                    rounding=ROUND_HALF_UP,
                ),
            },
            status=400,
        )
    if coupon_object.is_valid_for_course(course_with_code):
        coupon_object.students.add(student)
        new_price = Decimal(coupon_object.course.payable_amount) * Decimal(
            1 - (coupon_object.discount_percent / 100),
        )
        profile_cart.total_price = new_price
        profile_cart.save()
        return JsonResponse(
            {
                "message": "Coupon applied successfully.",
                "newPrice": profile_cart.total_price.quantize(
                    Decimal("0.01"),
                    rounding=ROUND_HALF_UP,
                ),
                "discount": coupon_object.discount_percent,
            },
            status=200,
        )

    return JsonResponse({"message": "Coupon is not valid for this cart."}, status=400)
