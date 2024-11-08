from django.shortcuts import render
from django.views.generic import TemplateView


# Create your views here.
class StudentDashboardView(TemplateView):
    template_name = "students/dashboard.html"

class StudentPurchasedCoursesView(TemplateView):
    template_name = "students/purchases.html"


class StudentMessagesView(TemplateView):
    template_name = "students/messages.html"


class StudentNotificationsView(TemplateView):
    template_name = "students/notifications.html"


class StudentReviewsView(TemplateView):
    template_name = "students/reviews.html"



class StudentCertificateView(TemplateView):
    template_name = "students/certificates.html"



class StudentTransactionView(TemplateView):
    template_name = "students/statements.html"



class StudentCreditView(TemplateView):
    template_name = "students/credits.html"


