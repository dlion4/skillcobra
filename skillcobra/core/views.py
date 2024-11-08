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
