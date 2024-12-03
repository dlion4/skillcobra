from datetime import timedelta

from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.utils import timezone
from django.views.generic import TemplateView

from skillcobra.school.models import Category, Course, CourseSubscription, Subscription
from skillcobra.users.models import Profile


class AuthorizedHomeViewMixin(LoginRequiredMixin, TemplateView):
    def get_profile(self):
        return self.request.user.user_profile
    def get_dashboard_url(self):
        if self.request.user.role == "student":
            return str(reverse("students:dashboard"))
        return str(reverse("instructors:dashboard"))

    def get_courses(self):
        return Course.objects.filter(status="approved").order_by("?")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["profile"] = self.get_profile()
        context["dashboard_url"] = self.get_dashboard_url()
        context["courses"] = self.get_courses()
        return context


# Create your views here.
class HomeView(AuthorizedHomeViewMixin):
    template_name = "pages/home.html"
    course = Course
    def get_newest_course(self):
        last_seven_days = timezone.now() - timedelta(days=7)
        return (Course.objects.filter(created_at__gt=last_seven_days))
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["newest_courses"] = self.get_newest_course()
        context["featured_courses"] = self.get_newest_course()
        context["popular_tutors"] = self.get_popular_tutors()
        return context
    def get_popular_tutors(self):
        return Profile.objects.filter(user__role="instructor").order_by("?")


class HomeExploreView(AuthorizedHomeViewMixin):
    template_name = "pages/explore.html"
    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)


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


class SiteMapView(AuthorizedHomeViewMixin):
    template_name = "pages/sitemap.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        return context

# added urls for this views



class DevelopersView(AuthorizedHomeViewMixin):
    template_name = "pages/onboarding/developers.html"

class OnboardingView(AuthorizedHomeViewMixin):
    template_name = "pages/onboarding/onboarding.html"

class HelpPageView(AuthorizedHomeViewMixin):
    template_name = "pages/helppage.html"

class StudentOrderView(AuthorizedHomeViewMixin):
    template_name = "pages/studentorder.html"

class StudentFormView(AuthorizedHomeViewMixin):
    template_name = "pages/onboarding/studentform.html"

class EditorsView(AuthorizedHomeViewMixin):
    template_name = "pages/tools/editors.html"

class AIView(AuthorizedHomeViewMixin):
    template_name = "pages/tools/ai.html"

class FilesView(AuthorizedHomeViewMixin):
    template_name = "pages/tools/files.html"

class VirtualLearningView(AuthorizedHomeViewMixin):
    template_name = "pages/tools/virtuallearning.html"

class CareerspageView(AuthorizedHomeViewMixin):
    template_name = "pages/careerspage.html"
    
class FreecourseView(AuthorizedHomeViewMixin):
    template_name = "pages/freecourse.html"
    
class CertView(AuthorizedHomeViewMixin):
    template_name = "pages/cert.html"
    
    
class VerificationView(AuthorizedHomeViewMixin):
    template_name = "pages/verification.html"
    
class StatementView(AuthorizedHomeViewMixin):
    template_name = "pages/statement.html"
    
    
class TestView(AuthorizedHomeViewMixin):
    template_name = "pages/testpage.html"
#pdf files
class PdreaderpageView(AuthorizedHomeViewMixin):
    template_name = "pages/tools/aitools/pdreaderpage.html"
    
    
class PdreaderView(AuthorizedHomeViewMixin):
    template_name = "pages/tools/pdreader.html"
    #inner tool pages
    
class ChataiView(AuthorizedHomeViewMixin):
    template_name = "pages/tools/aitools/chatai.html"

class CoursecreatorView(AuthorizedHomeViewMixin):
    template_name = "pages/tools/aitools/coursecreator.html"

class CourseassessView(AuthorizedHomeViewMixin):
    template_name = "pages/tools/aitools/courseassess.html"

class FilemanagerView(AuthorizedHomeViewMixin):
    template_name = "pages/tools/file/filemanager.html"
    