import pickle
from pathlib import Path

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from sklearn.feature_extraction.text import CountVectorizer

# Create your models here.
from config.settings.base import BASE_DIR


class Notification(models.Model):
    sender = models.ForeignKey(
        "users.Profile",
        related_name="notification_sender",
        on_delete=models.CASCADE,
    )
    receiver = models.ForeignKey(
        "users.Profile",
        related_name="notification_recipient",
        on_delete=models.CASCADE,
    )
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender} to {self.receiver}"


class Message(models.Model):
    sender = models.ForeignKey(
        "users.Profile",
        related_name="message_sender",
        on_delete=models.CASCADE,
    )
    receiver = models.ForeignKey(
        "users.Profile",
        related_name="message_recipient",
        on_delete=models.CASCADE,
    )
    title = models.CharField(max_length=255)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.sender} to {self.receiver}: {self.title}"


class PushSubscription(models.Model):
    profile = models.OneToOneField(
        "users.Profile",
        on_delete=models.CASCADE,
        related_name="profile_push_subscription",
    )
    endpoint = models.CharField(max_length=255)
    p256dh = models.CharField(max_length=255)
    auth = models.CharField(max_length=255)

    def __str__(self):
        return f"Push Subscription for {self.user.username}"


class Review(models.Model):
    profile = models.ForeignKey(
        "users.Profile",
        on_delete=models.CASCADE,
        related_name="profile_reviews",
    )
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField(blank=True, null=True)
    parent = GenericForeignKey("content_type", "object_id")
    rating = models.PositiveIntegerField()
    content = models.TextField()
    alert_message = models.CharField(max_length=355, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    profanity_score = models.PositiveBigIntegerField(default=0)
    is_verified = models.BooleanField(default=False)
    def __str__(self):
        return f"{self.profile} - {self.content_type.model} - {self.object_id}"

    def save(self, *args, **kwargs):
        with Path.open(str(BASE_DIR / "models" / "profanity_model.pkl"), "rb") as f:
            vectorizer, model = pickle.load(f)  # noqa: S301
        content_vector = vectorizer.transform([self.content])
        self.profanity_score = model.predict_proba(content_vector)[0][1]*100
        profanity_limit_score = 40
        if self.profanity_score > profanity_limit_score:
            self.is_verified = False
            self.alert_message = "[Profanity Detected]"
        else:
            self.is_verified = True
            self.alert_message = ""
        super().save(*args, **kwargs)


class ProfanityModel(models.Model):
    """Model for storing profanity model."""
    message = models.CharField(max_length=100)
    profanity_score = models.PositiveBigIntegerField(default=0)
    def __str__(self):
        return f"Profanity! <{self.profanity_score}>: {self.message}"


class Enrollment(models.Model):
    """Model for storing enrollment."""
    profile = models.ForeignKey(
        "users.Profile",
        on_delete=models.CASCADE,
        related_name="profile_enrollments",
    )
    email_address = models.EmailField(
        max_length=255,
        unique=True,
        verbose_name="Email Address",
    )
    # course = models.ForeignKey(
    #     "courses.Course",
    #     on_delete=models.CASCADE,
    #     related_name="course_enrollments",
    # )
    timestamp = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.profile} - {self.email_address}"
