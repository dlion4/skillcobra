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
    path(
        "assessment-view/",
        views.AssessmentView.as_view(),
        name="assessment_view",
    ),
    path(
        "certification-view/",
        views.CertificationView.as_view(),
        name="certification_view",
    ),
    path(
        "editors/",
        views.EditorListView.as_view(),
        name="editors_view",
    ),
    path(
        "ai-tools/",
        views.ArtificialIntelligenceToolsView.as_view(),
        name="ai_tools_view",
    ),
    path(
        "distant-learning/",
        views.VirtualLearningView.as_view(),
        name="distant_learning",
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
    path(
        "careers/",
        include("skillcobra.core.careers.urls", namespace="careers"),
    ),
]
