from django.urls import include
from django.urls import path

app_name = "students"
urlpatterns = [
    path("", include("roles.students.students.urls")),
]
