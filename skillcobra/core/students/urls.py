from django.urls import path

from . import views

app_name = "profile_students"
urlpatterns = [
    path(
        "save-course-liked/course_<course_pk>/course_<course_slug>/save_course/",
        views.SaveCourseView.as_view(),
        name="course_save_view",
    ),
    path(
        "un-save-course-liked/course_<course_pk>/course_<course_slug>/unsave_course/",
        views.RemoveSavedCourseView.as_view(),
        name="course_unsave_view",
    ),
    path(
        "un-save-all-courses-liked/",
        views.RemoveAllSavedCoursesView.as_view(),
        name="all_course_unsave_view",
    ),
]
