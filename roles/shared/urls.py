from django.urls import path

from skillcobra.memberships.views import MembershipPaymentView
from skillcobra.memberships.views import MembershipView

app_name = "shared"
urlpatterns = [
    path(
        "",
        MembershipView.as_view(),
        name="membership_view",
    ),
    path(
        "payment/<pk>/<name>/",
        MembershipPaymentView.as_view(),
        name="membership_payment_view",
    ),
]
