from decimal import Decimal
from django.db import models

# Create your models here.


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
