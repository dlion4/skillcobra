from datetime import timedelta

from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.utils import timezone
from django.views.generic import TemplateView

from skillcobra.school.models import Course, CourseSubscription, Subscription
from skillcobra.users.models import Profile


class AuthorizedHomeViewMixin(LoginRequiredMixin, TemplateView):
    def get_profile(self):
        return self.request.user.user_profile
    def get_dashboard_url(self):
        if self.request.user.role == "student":
            return str(reverse("students:dashboard"))
        return str(reverse("instructors:dashboard"))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["profile"] = self.get_profile()
        context["dashboard_url"] = self.get_dashboard_url()
        return context


# Create your views here.
class HomeView(AuthorizedHomeViewMixin):
    template_name = "pages/home.html"
    course = Course
    def get_newest_course(self):
        last_seven_days = timezone.now() - timedelta(days=7)
        return (
            Course.objects.filter(created_at__gte=last_seven_days)
            .filter(status="approved")
            .order_by(
                "-created_at",
            )
        )
    def get_courses(self):
        return Course.objects.filter(status="approved").order_by("?")
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["newest_courses"] = self.get_newest_course()
        context["featured_courses"] = self.get_newest_course()
        context["courses"] = self.get_courses()
        context["popular_tutors"] = self.get_popular_tutors()
        return context
    def get_popular_tutors(self):
        return Profile.objects.filter(user__role="instructor").order_by("?")


class HomeExploreView(AuthorizedHomeViewMixin):
    template_name = "pages/explore.html"


class HomeHelpView(AuthorizedHomeViewMixin):
    template_name = "pages/help.html"


class HomeReportView(AuthorizedHomeViewMixin):
    template_name = "pages/reports.html"


class HomeFeedbackView(AuthorizedHomeViewMixin):
    template_name = "pages/feedback.html"


class HomeAboutUsView(AuthorizedHomeViewMixin):
    template_name = "pages/about.html"


class HomePressView(AuthorizedHomeViewMixin):
    template_name = "core/press.html"


class HomeCareerView(AuthorizedHomeViewMixin):
    template_name = "core/career.html"


class HomeCompanyView(AuthorizedHomeViewMixin):
    template_name = "core/company.html"


class HomeContactView(AuthorizedHomeViewMixin):
    template_name = "pages/contact.html"


class HomeComingSoonView(AuthorizedHomeViewMixin):
    template_name = "pages/coming_soon.html"


class HomeTermsOfUseView(AuthorizedHomeViewMixin):
    template_name = "pages/terms.html"
