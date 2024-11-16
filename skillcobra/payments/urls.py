from django.urls import include
from django.urls import path

from .views import CheckPaymentStatusView
from .views import ProcessPaymentFormView

app_name = "payments"
urlpatterns = [
    path("process/", ProcessPaymentFormView.as_view(), name="pay"),
    path(
        "process/status/<student_pk>/", CheckPaymentStatusView.as_view(), name="status",
    ),
    path("membership/", include("roles.shared.urls", namespace="shared")),
]
