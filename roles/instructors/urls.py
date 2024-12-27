from django.urls import include
from django.urls import path

app_name = "instructors"
urlpatterns = [
    path("", include("roles.instructors.instructor.urls")),
    path("payments/", include("roles.instructors.payment.urls", namespace="payments")),
]
