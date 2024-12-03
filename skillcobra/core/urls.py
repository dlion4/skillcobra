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
    
    # neww urls for added pages


    path("developers/", views.DevelopersView.as_view(), name="developers"),
    path("onboarding/", views.OnboardingView.as_view(), name="onboarding"),
    path("helppage/", views.HelpPageView.as_view(), name="helppage"),
    path("studorder/", views.StudentOrderView.as_view(), name="studorder"),
    path("studentform/", views.StudentFormView.as_view(), name="studentform"),
    path("editors/", views.EditorsView.as_view(), name="editors"),
    path("ai/", views.AIView.as_view(), name="ai"),
    path("files/", views.FilesView.as_view(), name="files"),
    path("careerspage/", views.CareerspageView.as_view(), name="careerspage"),
    path("virtuallearning/", views.VirtualLearningView.as_view(), name="virtuallearning"),
    path("freecourse/", views.FreecourseView.as_view(), name="freecourse"),
    
    path("cert/", views.CertView.as_view(), name="cert"),
    path("test/", views.TestView.as_view(), name="test"),
    path("verification/", views.VerificationView.as_view(), name="verification"),
    path("statement/", views.StatementView.as_view(), name="statement"),
    #neww section pdfs
    path("pdreader/", views.PdreaderView.as_view(), name="pdreader"),
    path("pdreaderpage/", views.PdreaderpageView.as_view(), name="pdreaderpage"),
    #inner tool pages
    
    path("chatai/", views.ChataiView.as_view(), name="chatai"),
    path("coursecreator/", views.CoursecreatorView.as_view(), name="coursecreator"),
    path("courseassess/", views.CourseassessView.as_view(), name="courseassess"),
    path("filemanager/", views.FilemanagerView.as_view(), name="filemanager")

    

]