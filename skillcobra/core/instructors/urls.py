from django.urls import path

from .actions import create_discussion
from .actions import delete_discussion
from .actions import subscribe_to_tutor
from .views import InstructorProfileView

app_name = "profile_instructors"
urlpatterns = [
    path(
        "<pk>/<username>/",
        InstructorProfileView.as_view(),
        name="instructor_view",
    ),
    path(
        "<tutor_pk>/<tutor__user_username>/create_discussion",
        create_discussion,
        name="create_discussion_view",
    ),
    path(
        "discussions/<discussion_pk>/discussion/delete/",
        delete_discussion,
        name="delete_discussion_view",
    ),
    path(
        "subscription/<tutor_pk>/subscribe/",
        subscribe_to_tutor,
        name="subscribe_to_tutor_view",
    ),
]
