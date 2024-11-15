from rest_framework import serializers

from .models import CourseSubscription
from .models import Subscription


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = "__all__"
class CourseSubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseSubscription
        fields = "__all__"
