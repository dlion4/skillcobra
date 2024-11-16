from django.urls import path

from .views import LoginView
from .views import LogoutView
from .views import RegisterView
from .views import RequestPasswordResetView
from .views import UpdateProfileView
from .views import UpdateProfileAddressView
from .views import CreatePayoutAccountView

app_name = "users"
urlpatterns = [
    path("login/", view=LoginView.as_view(), name="login"),
    path("logout/", view=LogoutView.as_view(), name="logout"),
    path("register/", view=RegisterView.as_view(), name="register"),
    path("profile-update/", view=UpdateProfileView.as_view(), name="update_profile"),
    path(
        "profile-update/address/",
        view=UpdateProfileAddressView.as_view(),
        name="update_profile_address",
    ),
    path(
        "profile-create-payout-account/",
        view=CreatePayoutAccountView.as_view(),
        name="create_profile_payout_account_view",
    ),
    path(
        "password-reset-request/",
        view=RequestPasswordResetView.as_view(),
        name="req_password_reset_view",
    ),
]
