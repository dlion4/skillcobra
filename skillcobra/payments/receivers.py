# receivers.py

import requests
from django.dispatch import receiver
from django.urls import reverse

from .middleware import get_request
from .signals import payment_initiated


@receiver(payment_initiated)
def handle_payment_initiated(sender, **kwargs):
    student = kwargs.get("student")
    parent = kwargs.get("parent")
    payment_details = kwargs.get("payment_details")
    print(kwargs.items())
    payment_status_url = reverse(
        "payments:status",
        kwargs={
            "student_pk": student.pk,
        },
    )
    data = {
        "student_pk": student.pk,
        "parent_pk": parent.pk,
        "payment_details": payment_details,
    }
    try:
        response = requests.post(
            f"http://localhost:8002/{payment_status_url}",
            json=data,
            timeout=3,
        )
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error sending payment initiation event: {e}")
