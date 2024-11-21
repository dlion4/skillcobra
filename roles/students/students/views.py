from datetime import timedelta

from django.db.models import Count
from django.utils import timezone

from roles.instructors.instructor.models import ScheduleClass
from skillcobra.payments.forms import CoursePurchasePaymentForm
from skillcobra.school.models import Course
from skillcobra.school.models import CourseSubscription
from skillcobra.school.models import SavedCourse
from skillcobra.school.models import Subscription
from skillcobra.users.forms import UpdateAccountProfileBasicDataForm

from .utils import TemplateViewMixin


# Create your views here.
class StudentDashboardView(TemplateViewMixin):
    template_name = "dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["new_course"] = self.latest_courses()
        context["tutor_subscribed_to"] = self.get_number_of_tutors_for_student()
        context["recent_subscriptions"] = self.recent_tutor_subscriptions()
        return context

    def latest_courses(self):
        time_limit = timezone.now() - timedelta(days=7)
        return Course.objects.prefetch_related("tutor").filter(
            created_at__gte=time_limit,
        )
    def recent_tutor_subscriptions(self):
        time_limit = timezone.now() - timedelta(days=30)
        return (
            CourseSubscription.objects.prefetch_related("subscription")
            .filter(
                student=self.get_profile(),
                date_subscribed__gte=time_limit,
            )
            .order_by("-date_subscribed")
        )

    def get_number_of_tutors_for_student(self):
        try:
            subscriptions = Subscription.objects.filter(
                students=self.get_profile(),
            ).aggregate(
                tutor_count=Count("tutor", distinct=True),
            )
            return subscriptions["tutor_count"]
        except Subscription.DoesNotExist:
            return "0"


class StudentProfileUpdateView(TemplateViewMixin):
    template_name = "profile.html"
    account_basic_form = UpdateAccountProfileBasicDataForm
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["account_basic_update_form"] = self.account_basic_form(
            instance=self.get_profile(),
        )
        return context


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


class LessonHomeView(TemplateViewMixin):
    template_name = "lessons.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["schedule_classes"] = ScheduleClass.objects.filter(
            courses_id__in=self.get_profile().purchased_courses.all(),
        )
        return context
