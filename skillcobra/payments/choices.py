from django.db import models


class TransactionStatus(models.TextChoices):
    PENDING = "pending", "Pending"
    SUCCESS = "success", "Success"
    FAILED = "failed", "Failed"
class TransactionIntentChoices(models.TextChoices):
    CP = "cp", "Course Purchase"
    SP = "sp", "Service Purchase"
    MP = "mp", "Membership Purchase"
    MS = "ms", "Monthly Subscription"