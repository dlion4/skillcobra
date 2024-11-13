from typing import ClassVar

from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.db.models import EmailField
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from skillcobra.purchases.models import Cart

from .managers import UserManager


class User(AbstractUser):
    """
    Default custom user model for skillcobra.
    If adding fields that need to be filled at user signup,
    check forms.SignupForm and forms.SocialSignupForms accordingly.
    """

    # First and last name do not cover name patterns around the globe
    email = EmailField(_("email address"), unique=True)
    username = models.CharField(_("username"), max_length=100, blank=True)
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

    def save(self, *args, **kwargs):
        if not self.username:
            self.username = self.email[: self.email.index("@")]
        super().save(*args, **kwargs)


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


class Profile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="user_profile"
    )
    first_name = models.CharField(max_length=200, blank=True)
    last_name = models.CharField(max_length=200, blank=True)
    headline = models.CharField(max_length=200, blank=True)
    bio = models.TextField(blank=True)

    def __str__(self):
        return self.user.email

    def full_name(self):
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.user.username

    def get_public_profile_url(self):
        return reverse(
            "profile_instructors:instructor_view",
            kwargs={
                "pk": self.pk,
                "username": self.user.username,
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
            return []
    def get_subscription_url(self):
        return reverse(
            "profile_instructors:subscribe_to_tutor_view",
            kwargs={
                "tutor_pk": self.pk,
            },
        )

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
