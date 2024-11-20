import random
import string
from django.core.exceptions import ValidationError
from decimal import Decimal

from django.db import models
from django.utils import timezone

# Create your models here.

class CouponManager(models.Manager):
    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(
                start_timestamp__lte=timezone.now(),
                ended_timestamp__gte=timezone.now(),
            )
        )


class Cart(models.Model):
    student = models.OneToOneField(
        "users.Profile",
        on_delete=models.CASCADE,
        related_name="student_cart",
    )
    courses = models.ManyToManyField("school.Course", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
    )

    def __str__(self):
        return f"Cart #{self.id} <{self.student.full_name()}>"

    def save(self, *args, **kwargs):
        self.total_price = self.total_price_
        super().save(*args, **kwargs)

    @property
    def total_price_(self):
        try:
            return sum(course.payable_amount for course in self.courses.all())
        except Exception:  # noqa: BLE001
            return Decimal("0.00")


class Coupon(models.Model):
    course = models.ForeignKey(
        "school.Course",
        on_delete=models.CASCADE,
        related_name="coupons",
    )
    code = models.CharField(max_length=255, unique=True)
    discount_percent = models.PositiveIntegerField()
    start_timestamp = models.DateTimeField()
    ended_timestamp = models.DateTimeField()
    students = models.ManyToManyField(
        "users.Profile",
        blank=True,
        related_name="applied_coupons",
        limit_choices_to={"user__role": "student"},
    )
    admin_objects = models.Manager()
    objects = CouponManager()
    class Meta:
        verbose_name = "Coupon"
        verbose_name_plural = "Coupons"
        ordering = ("-start_timestamp",)
        constraints = [
            models.CheckConstraint(
                check=models.Q(start_timestamp__lte=models.F("ended_timestamp")),
                name="coupon_start_timestamp_lte_ended_timestamp",
            ),
            models.UniqueConstraint(
                fields=["course", "code"],
                name="unique_coupon_per_course",
            ),
        ]

    def __str__(self):
        return f"Coupon #{self.id}: {self.code} for {self.course.title}"
    def save(self, *args, **kwargs):
        self.clean()
        if not self.code:
            self.code = self.generate_code()
        super().save(*args, **kwargs)
    def clean(self):
        if self.course.status != "approved":
            msg = "Can only create coupon code for approved courses"
            raise ValidationError(msg)
        return super().clean()

    def generate_code(self):
        population = str(string.ascii_uppercase + string.digits + str(self.course.pk))
        return "".join(random.choices(population, k=8))  # noqa: S311
    @property
    def is_active(self):
        """Check if the coupon is active."""
        return self.start_timestamp <= timezone.now() <= self.ended_timestamp
    def is_valid_for_course(self, course):
        """Check if the coupon is valid for the course."""
        return self.course == course and self.is_active
    def is_valid_for_student(self, student):
        """Check if the coupon is valid for the student."""
        return student in self.students.all() or student in self.course.students.all()
