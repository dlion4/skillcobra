from django.urls import path

from . import views

app_name = "shared"
urlpatterns = [
    path(
        "",
        views.StudentMembershipView.as_view(),
        name="membership_view",
    ),
    path(
        "payment/",
        views.StudentMembershipPurchaseView.as_view(),
        name="membership_payment_view",
    ),
]
