from rest_framework import serializers

from skillcobra.users.serializers import ProfileSerializer

from .models import Message


class MessageSerializer(serializers.ModelSerializer):
    sender = ProfileSerializer(read_only=True)
    receiver = ProfileSerializer(read_only=True)
    class Meta:
        model = Message
        fields = "__all__"
