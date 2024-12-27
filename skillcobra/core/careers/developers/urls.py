from django.urls import path

from . import views

app_name = "developers"

urlpatterns = [
    path(
        "recruitment/",
        views.DeveloperRecruitmentView.as_view(),
        name="developer_recruitment_view",
    ),
]
