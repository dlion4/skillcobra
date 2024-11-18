import time
from datetime import timedelta
from decimal import Decimal
from typing import ClassVar

from django.contrib.auth.models import AbstractUser, AbstractBaseUser, PermissionsMixin
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.db.models import EmailField
from django.db.models import Sum
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from roles.instructors.instructor.models import CourseSale
from skillcobra.purchases.models import Cart
from skillcobra.school.models import Course
from skillcobra.school.models import CourseSubscription
from skillcobra.school.models import Subscription

from .managers import UserManager


class User(AbstractUser):
    """
    Default custom user model for skillcobra.
    If adding fields that need to be filled at user signup,
    check forms.SignupForm and forms.SocialSignupForms accordingly.
    """
    # First and last name do not cover name patterns around the globe
    email = EmailField(_("email address"), unique=True)
    username = None
    ROLE_CHOICES = [
        ("student", "Student"),
        ("instructor", "Instructor"),
        ("superadmin", "SuperAdmin"),
    ]
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
    )
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects: ClassVar[UserManager] = UserManager()

    def __str__(self):
        return self.email


# models.py
class Student(User):
    class Meta:
        proxy = True
        verbose_name = "Student"


class Instructor(User):
    class Meta:
        proxy = True
        verbose_name = "Instructor"


class SuperAdmin(User):
    class Meta:
        proxy = True
        verbose_name = "SuperAdmin"


def upload_avatar_to_(instance, filename):
    return f"profile/avatar/{instance.user.username}/{time.time()}_{filename}"


class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="user_profile",
    )
    first_name = models.CharField(max_length=200, blank=True)
    last_name = models.CharField(max_length=200, blank=True)
    headline = models.CharField(max_length=200, blank=True)
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to=upload_avatar_to_, blank=True, null=True)
    purchased_courses = models.ManyToManyField(
        "school.Course",
        blank=True,
        related_name="purchased_courses",
    )
    username = models.CharField(max_length=255, blank=True, null=True)  # noqa: DJ001

    def __str__(self):
        return self.user.email

    def full_name(self):
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.username

    def get_public_profile_url(self):
        return reverse(
            "profile_instructors:instructor_view",
            kwargs={
                "pk": self.pk,
                "username": self.username,
            },
        )
    def get_create_discussion_url(self):
        return reverse(
            "profile_instructors:create_discussion_view",
            kwargs={
                "tutor_pk": self.pk,
                "tutor__user_username": self.user.username,
            },
        )

    def get_all_courses(self):
        return self.course_tutor.all()

    def get_up_coming_courses(self):
        return self.course_tutor.filter(course_release_date__gte=timezone.now())

    def get_discussions(self):
        return (
            self.tutor_discussion_profile.prefetch_related("tutor")
            .filter(is_active=True)
            .order_by(
                "-created_at",
            )
        )

    def get_saved_courses(self):
        try:
            return self.student_saved_course.courses.all()
        except ObjectDoesNotExist:
            return []

    def get_all_cart_items(self):
        try:
            return Cart.objects.get(student=self).courses.all()
        except ObjectDoesNotExist:
            print("No Cart object found; returning empty QuerySet.")
            return Course.objects.none()

    def get_subscription_url(self):
        return reverse(
            "profile_instructors:subscribe_to_tutor_view",
            kwargs={
                "tutor_pk": self.pk,
            },
        )

    def received_messages(self):
        return self.message_recipient.filter(is_read=False)[:3]

    def get_all_received_messages(self):
        return self.message_recipient.filter(is_read=False)

    def get_subscribed_tutor_ids(self):
        # Get the IDs of tutors that this student is subscribed to
        ids = CourseSubscription.objects.filter(student=self).values_list(
            "subscription__tutor_id",
            flat=True,
        )
        return [Profile.objects.filter(pk=ids).first() for ids in ids]

    def get_tutor_latest_sales(self):
        try:
            return self._extracted_from_get_tutor_total_sales_3()
        except ObjectDoesNotExist:
            return Decimal("0.00")

    def get_tutor_total_sales(self):
        try:
            return self._extracted_from_get_tutor_total_sales_3()
        except CourseSale.DoesNotExist:
            return Decimal("0.00")

    # TODO Rename this here and in `get_tutor_latest_sales` and `get_tutor_total_sales`
    def _extracted_from_get_tutor_total_sales_3(self):
        sales = self.tutor_sales.transactions.aggregate(total_sales=Sum("amount"))
        if sales["total_sales"] is None:
            return Decimal("0.00")
        return sales["total_sales"]

    def get_tutor_sales(self):
        return self.tutor_sales.courses.all()

    def get_subscribed_courses_per_tutor(self):
        if tutor_subscription := Subscription.objects.filter(
            students=self,
        ).first():
            # Return the list of Course instances that the tutor is associated with
            return len([
                course_sub.course
                for course_sub in CourseSubscription.objects.filter(
                    subscription=tutor_subscription,
                )
            ])
        return 0
    def get_purchased_courses_by_student_per_tutor(self):
        return self.purchased_courses.filter(tutor=self).all()


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance:User, created, **kwargs):
    if created:
        profile = Profile.objects.create(user=instance)
        profile.username =  instance.email[: instance.email.index("@")]
        profile.save()
