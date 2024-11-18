from django.contrib.auth import get_user
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET
from django.views.decorators.http import require_POST

from skillcobra.core.instructors.decorator import discussion_wrapper
from skillcobra.school.forms import DiscussionForm
from skillcobra.school.forms import DiscussionReplyForm
from skillcobra.school.models import (
    Course,
    CourseSubscription,
    Discussion,
    Subscription,
)
from skillcobra.users.models import Profile
from django.db import transaction


@csrf_exempt
@require_POST
@login_required
def create_discussion(request, tutor_pk=None, tutor__user_username=None):
    tutor = get_object_or_404(
        Profile,
        pk=tutor_pk,
        username=tutor__user_username,
    )
    profile = get_user(request).user_profile
    form = DiscussionForm(request.POST)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.tutor = tutor
        instance.student = profile
        instance.save()
        form.save()
        return render(
            request,
            "instructors/components/partials/discussion.html",
            {"item": instance},
        )
    return render(
        request,
        "instructors/components/partials/discussion.html",
        {"form": form},
    )


@login_required
@csrf_exempt
@require_GET
@discussion_wrapper
def delete_discussion(request, discussion_pk):
    request.discussion.is_active = False
    request.discussion.save()
    return JsonResponse({}, status=201)


@login_required
@transaction.atomic
def message_tutor(request, tutor_pk):
    pass
@login_required
@transaction.atomic
def subscribe_to_tutor(request, tutor_pk):
    tutor = get_object_or_404(Profile, pk=tutor_pk)
    student = (
        request.user.user_profile
    )  # Assuming user_profile is the related name for Profile

    # Get or create a subscription for the tutor
    subscription, created = Subscription.objects.get_or_create(tutor=tutor)
    tutor_courses = Course.objects.filter(tutor=tutor)

    existing_subscriptions = set(
        CourseSubscription.objects.filter(
            subscription=subscription, student=student,
        ).values_list("course_id", flat=True),
    )

    if course_subscriptions := [
        CourseSubscription(
            subscription=subscription, student=student, course=course,
        )
        for course in tutor_courses
        if course.id not in existing_subscriptions
    ]:
        CourseSubscription.objects.bulk_create(course_subscriptions)
    return JsonResponse(
        {"subscriptions": str(subscription.students.all().count())},
        status=201,
        safe=False,
    )
