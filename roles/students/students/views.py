from skillcobra.payments.forms import CoursePurchasePaymentForm
from skillcobra.school.models import SavedCourse

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

class StudentSavedCoursesView(TemplateViewMixin):
    template_name = "saved_course.html"
    model = SavedCourse
    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)

class StudentShoppingCartView(TemplateViewMixin):
    template_name = "shopping_cart.html"
    payment_form = CoursePurchasePaymentForm
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["payment_form"] = self.payment_form(profile=self.get_profile())
        return context

