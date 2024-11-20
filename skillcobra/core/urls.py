from django.urls import include
from django.urls import path

from . import views

urlpatterns = [
    path(
        "",
        views.HomeView.as_view(),
        name="home",
    ),
    path(
        "site-maps",
        views.SiteMapView.as_view(),
        name="sitemap",
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
    path(
        "about/",
        views.HomeAboutUsView.as_view(),
        name="about",
    ),
    path(
        "press/",
        views.HomePressView.as_view(),
        name="press",
    ),
    path(
        "career/",
        views.HomeCareerView.as_view(),
        name="career",
    ),
    path(
        "company/",
        views.HomeCompanyView.as_view(),
        name="company",
    ),
    path(
        "contact-us/",
        views.HomeContactView.as_view(),
        name="contact",
    ),
    path(
        "coming-soon/",
        views.HomeComingSoonView.as_view(),
        name="soon",
    ),
    path(
        "terms-of-use/",
        views.HomeTermsOfUseView.as_view(),
        name="terms",
    ),
    # COURSE URL
    path("courses/", include("skillcobra.core.courses.urls", namespace="courses")),
    path(
        "instructors/",
        include("skillcobra.core.instructors.urls", namespace="profile_instructors"),
    ),
    path(
        "students/",
        include("skillcobra.core.students.urls", namespace="profile_students"),
    ),
]
