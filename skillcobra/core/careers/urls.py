from django.urls import include
from django.urls import path

app_name = "careers"
urlpatterns = [
    path(
        "developers/",
        include("skillcobra.core.careers.developers.urls", namespace="developers"),
    ),
]
