from django.urls import path

from .views import build_subscribers_bar_chart_view

urlpatterns = [
    path("analytics/<tutor_pk>/", build_subscribers_bar_chart_view, name="fetcher_analytics"),
]
