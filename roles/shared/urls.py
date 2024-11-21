from django.urls import path

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
    path("ide/", views.WebEditorView.as_view(), name="web_editor_view"),
    path("ide/execute", views.execute_code, name="execute_code_view"),
]
