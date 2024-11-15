from datetime import datetime

from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.db.models import Avg
from django.db.models import Count
from django.db.models import Q
from django.db.models import Sum
from django.http import JsonResponse
from django.utils import timezone

from skillcobra.school.models import CourseSubscription
from skillcobra.school.models import Subscription
from skillcobra.school.serializers import CourseSubscriptionSerializer
from skillcobra.school.serializers import SubscriptionSerializer


def build_subscribers_bar_chart_view(request, tutor_pk):
    try:
        subscription = Subscription.objects.get(tutor__pk=tutor_pk)
        course_subscriptions = CourseSubscription.objects.filter(
            subscription=subscription,
        )
        monthly_counts = [0] * 12
        for subscription in course_subscriptions.distinct():
            month = (
                subscription.date_subscribed.month
            )
            monthly_counts[month - 1] += 1
        return JsonResponse({"data": monthly_counts})
    except ObjectDoesNotExist:
        return JsonResponse({"data": [0] * 12})
