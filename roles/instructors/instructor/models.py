from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from froala_editor.fields import FroalaField
from hashids import Hashids

from roles.instructors.instructor.choices import AccountIntentChoice
from skillcobra.payments.models import Transaction
from skillcobra.school.models import Course

# Create your models here.


def validate_intent_reason(value):
    """
    Custom validation for intent_reason based on the intent field.
    """
    if not hasattr(value, "instance"):
        return
    account = value.instance
    if not value.strip() and account.intent in [
        AccountIntentChoice.R,
        AccountIntentChoice.P,
    ]:
        msg = f"Intent Reason is required for this {account.intent} intent."
        raise ValidationError(msg)


def validate_tutor_role(value):
    course_sale = value.instance
    if not hasattr(value, "instance"):
        return
    if course_sale.user.role != "instructor":
        msg = "This instance must be a tutor to proceed!"
        raise ValidationError(msg)


class CourseSale(models.Model):
    tutor = models.OneToOneField(
        "users.Profile",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="tutor_sales",
        validators=[validate_tutor_role],
    )
    transactions = models.ManyToManyField(
        Transaction,
        related_name="course_sales",
        blank=True,
    )
    courses = models.ManyToManyField(
        Course,
        related_name="sales_course",
        blank=True,
    )
    timestamp = models.DateTimeField(auto_now_add=True)
    modified_timestamp = models.DateTimeField(auto_now=True)
    is_cancelled = models.BooleanField(default=False)

    def __str__(self):
        return f"Course Sale: {self.course.title} - Tutor: {self.tutor.user.username}"


class Account(models.Model):
    holder = models.OneToOneField(
        "users.Profile",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="profile_bank_account",
    )
    intent = models.CharField(
        max_length=10,
        choices=AccountIntentChoice.choices,
        default=AccountIntentChoice.D,
    )
    intent_reason = models.CharField(
        max_length=300,
        blank=True,
        validators=[validate_intent_reason],
    )
    account_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"Bank Account for {self.holder.full_name()}"


class ScheduleClass(models.Model):
    courses = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="course_live_links",
    )
    class_live_link = models.CharField(max_length=255)
    login_required = models.BooleanField(default=False)
    lesson_overview = FroalaField(
        help_text="Login credentials for the lesson",
    )
    credentials = FroalaField(
        help_text="Login credentials for the lesson",
    )
    class_start_time = models.DateTimeField()
    class_end_time = models.DateTimeField()
    short_url = models.CharField(max_length=27, blank=True)

    class Meta:
        verbose_name = _("ScheduleClass")
        verbose_name_plural = _("ScheduleClasses")
        ordering = ["-class_start_time"]
        get_latest_by = "class_start_time"

    def __str__(self):
        return self.class_live_link

    def save(self, *args, **kwargs):
        if not self.short_url:
            hashids = Hashids(salt="skillcobra_schedule_class_salt", min_length=6)
            self.short_url = hashids.encode(self.pk or 0)
        super().save(*args, **kwargs)

    def get_remaining_time_to_class(self):
        current_time = timezone.now()
        remaining_time = self.class_start_time - current_time
        if remaining_time.total_seconds() <= 0:
            return "Class time has already passed"
        total_seconds = int(remaining_time.total_seconds())
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        return f"{hours} hr, {minutes} min, {seconds} sec"

    def get_short_url(self):
        return reverse(
            "courses:live_class_view",
            kwargs={
                "course_pk": self.courses.pk,
                "course_slug": self.courses.slug,
                "short_url": self.short_url,
                "schedule_pk": self.pk,
            },
        )

    def get_lesson_status(self):
        current_time = timezone.now()
        remaining_time = self.class_start_time - current_time
        if remaining_time.total_seconds() > 0:
            time_remaining = self.get_remaining_time_to_class()
            return f"Upcoming <br /> <div id='upcoming_time_counter_{self.pk}'>{time_remaining}</div>"  # noqa: E501
        courses_limit = 10800
        return (
            "live<span></span>"
            if abs(remaining_time.total_seconds()) <= courses_limit
            else "Ended"
        )
    def get_class_time_formatted(self):
        return self.class_start_time.strftime("%Y-%m-%d %H:%M:%S")
    def get_class_end_time(self):
        return self.class_end_time.strftime("%Y-%m-%d %H:%M:%S")
