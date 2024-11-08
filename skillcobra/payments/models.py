from django.db import models


class Plan(models.Model):
    name = models.CharField(
        max_length=1,
        unique=True, choices=(("B", "Basic"),("P", "Pro")),
        default="B",
    )
    price = models.DecimalField(
        max_digits=10, decimal_places=2, default=10.50)
    duration = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.get_name_display()} Plan"

class PlanFeature(models.Model):
    plan = models.ForeignKey(
        Plan, on_delete=models.CASCADE, related_name="plan_features")
    feature = models.CharField(max_length=100, unique=True)
    def __str__(self):
        return f"{self.plan.get_name_display()} Plan Feature"

# Create your models here.
class MemberShip(models.Model):
    profile = models.ForeignKey(
        "users.Profile",
        on_delete=models.CASCADE,
        related_name="profile_membership")
    plan = models.ForeignKey(
        Plan, on_delete=models.CASCADE, related_name="membership_plan")
    status = models.CharField(
        max_length=1,
        choices=(
            ("A", "Active"), ("I", "Inactive"),
            ("C", "Cancelled"), ("P", "Paused"),
            ),
        default="I",
    )
    is_paid = models.BooleanField(default=False)
    def __str__(self):
        return f"{self.profile.user.username} - {self.plan.get_name_display()} Plan"
