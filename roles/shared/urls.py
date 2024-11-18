from django.urls import path

from roles.shared.views import create_google_meet_event
from skillcobra.memberships.views import MembershipPaymentView
from skillcobra.memberships.views import MembershipView
from . import views


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
