from django.urls import path

from . import views

urlpatterns = [
    path(
        "",
        views.HomeView.as_view(),
        name="home",
    ),
    path(
        "explore/",
        views.HomeExploreView.as_view(),
        name="explore",
    ),
    path(
        "help/",
        views.HomeHelpView.as_view(),
        name="help",
    ),
    path(
        "report-history/",
        views.HomeReportView.as_view(),
        name="report-history",
    ),
    path(
        "feedback/",
        views.HomeFeedbackView.as_view(),
        name="feedback",
    ),
]
