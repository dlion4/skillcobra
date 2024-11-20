from django.urls import path

from . import views

app_name = "partials"
urlpatterns = [
    path(
        "filter-attendance/",
        views.get_attendance_data, name="filter_attendance_view"),
]
