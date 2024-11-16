from django.db import models


class AccountIntentChoice(models.TextChoices):
    D = "deposit", "Deposit"
    W = "withdrawal", "Withdrawal"
    R = "refund", "Refund"
    S = "salary", "Salary"
    P = "penalty", "Penalty"
    T = "transfer", "Transfer"
