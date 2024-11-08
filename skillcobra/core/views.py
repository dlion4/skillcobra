from django.shortcuts import render
from django.views.generic import TemplateView

# Create your views here.
class HomeView(TemplateView):
    template_name = "pages/home.html"
class HomeExploreView(TemplateView):
    template_name = "pages/explore.html"


class HomeHelpView(TemplateView):
    template_name = "pages/help.html"

class HomeReportView(TemplateView):
    template_name = "pages/reports.html"
class HomeFeedbackView(TemplateView):
    template_name = "pages/feedback.html"
class HomeAboutUsView(TemplateView):
    template_name = "pages/about.html"
class HomePressView(TemplateView):
    template_name = "core/press.html"
class HomeCareerView(TemplateView):
    template_name = "core/career.html"
class HomeCompanyView(TemplateView):
    template_name = "core/company.html"
class HomeContactView(TemplateView):
    template_name = "pages/contact.html"
class HomeComingSoonView(TemplateView):
    template_name = "pages/coming_soon.html"
class HomeTermsOfUseView(TemplateView):
    template_name = "pages/terms.html"
