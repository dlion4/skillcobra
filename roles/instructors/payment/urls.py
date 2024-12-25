from django.urls import path

from . import views

app_name = "payments"
urlpatterns = [
    path("payout/", views.initiate_payout_view, name="initiate_payout_view"),
    path(
        "balance-lookup/",
        views.account_balance_lookup_view,
        name="account_balance_lookup",
    ),
]
