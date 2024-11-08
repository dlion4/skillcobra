from django.urls import path

from . import views

urlpatterns = [
    path(
        "",
        views.StudentDashboardView.as_view(),
        name="dashboard",
    ),
    path(
        "purchased-courses/",
        views.StudentPurchasedCoursesView.as_view(),
        name="purchased-courses",
    ),
    path(
        "messages/",
        views.StudentMessagesView.as_view(),
        name="messages",
    ),
    path(
        "notifications/",
        views.StudentNotificationsView.as_view(),
        name="notifications",
    ),
    path(
        "reviews/",
        views.StudentReviewsView.as_view(),
        name="reviews",
    ),
    path(
        "certificates/",
        views.StudentCertificateView.as_view(),
        name="certificates",
    ),
    path(
        "credits/",
        views.StudentCreditView.as_view(),
        name="credits",
    ),
    path(
        "statements/",
        views.StudentTransactionView.as_view(),
        name="statements",
    ),
]
