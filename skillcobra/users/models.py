from typing import ClassVar

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import CharField
from django.db.models import EmailField
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

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
        default="student",
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

class Profile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="user_profile")

    def __str__(self):
        return self.user.email
