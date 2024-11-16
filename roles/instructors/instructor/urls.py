from django.urls import path

from . import views

urlpatterns = [
    path(
        "",
        views.InstructorDashboardView.as_view(),
        name="dashboard",
    ),
    path(
        "analytics/",
        views.InstructorAnalyticsView.as_view(),
        name="analytics",
    ),
    path(
        "stream-setup/",
        views.InstructorStreamingSetupView.as_view(),
        name="streaming_setup",
    ),
    path(
        "stream/live/",
        views.InstructorStreamingView.as_view(),
        name="streaming_live_view",
    ),
    path(
        "profile-update/",
        views.InstructorProfileUpdateView.as_view(),
        name="update_profile",
    ),
    path(
        "create-course/",
        views.InstructorCreatedCourseView.as_view(),
        name="create_course_view",
    ),
    path(
        "detail-course/<pk>/<slug>/",
        views.InstructorCourseDetailView.as_view(),
        name="detail_course_view",
    ),
]
