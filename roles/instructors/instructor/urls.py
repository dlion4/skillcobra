from django.urls import path

from . import views

urlpatterns = [
    path(
        "",
        views.InstructorDashboardView.as_view(),
        name="dashboard",
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
