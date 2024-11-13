from django.urls import include
from django.urls import path

from . import views

app_name = "school"
urlpatterns = [
    path(
        "courses/delete-module/<module_pk>/",
        views.delete_course_module,
        name="delete_course_module_view",
    ),
    path(
        "courses/delete-course/<course_pk>/<course_slug>/",
        views.delete_course_view,
        name="delete_course_view",
    ),
    path(
        "courses/update-module/<module_pk>/",
        views.update_course_module,
        name="update_course_module_view",
    ),
    path(
        "courses/create-lecture-for-module/<module_pk>/",
        views.create_course_module_lecture,
        name="create_course_module_view",
    ),
    path(
        "courses/update-lecture-for-module/<module_pk>/<lecture_pk>/",
        views.update_lecture_view,
        name="update_lecture_view",
    ),
    path(
        "courses/delete-lecture-for-module/<module_pk>/<lecture_pk>/",
        views.delete_lecture_view,
        name="delete_lecture_view",
    ),
]
