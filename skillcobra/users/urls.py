from django.urls import path

from .views import LoginView
from .views import LogoutView
from .views import RegisterView
from .views import RequestPasswordResetView
from .views import UpdateProfileView

app_name = "users"
urlpatterns = [
    path("login/", view=LoginView.as_view(), name="login"),
    path("logout/", view=LogoutView.as_view(), name="logout"),
    path("register/", view=RegisterView.as_view(), name="register"),
    path("profile-update/", view=UpdateProfileView.as_view(), name="update_profile"),
    path(
        "password-reset-request/",
        view=RequestPasswordResetView.as_view(),
        name="req_password_reset_view",
    ),
]
