from .utils import TemplateViewMixin


# Create your views here.
class StudentDashboardView(TemplateViewMixin):
    template_name = "dashboard.html"


class StudentPurchasedCoursesView(TemplateViewMixin):
    template_name = "purchases.html"


class StudentMessagesView(TemplateViewMixin):
    template_name = "messages.html"


class StudentNotificationsView(TemplateViewMixin):
    template_name = "notifications.html"


class StudentReviewsView(TemplateViewMixin):
    template_name = "reviews.html"


class StudentCertificateView(TemplateViewMixin):
    template_name = "certificates.html"


class StudentTransactionView(TemplateViewMixin):
    template_name = "statements.html"


class StudentCreditView(TemplateViewMixin):
    template_name = "credits.html"
