from django.views.generic import TemplateView
from django.contrib.contenttypes.models import ContentType
from skillcobra.memberships.models import Plan, Question


class StudentMembershipView(TemplateView):
    template_name = "membership/home.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["student_plan"] = Plan.objects.filter(name="S").first()
        context["instructor_plan"] = Plan.objects.filter(name="I").first()
        context["plan_questions"] = self.get_plan_questions()
        return context
    def get_plan_questions(self):
        plan_content_type = ContentType.objects.get_for_model(Plan)
        return (
            ContentType.objects.get_for_model(Question)
            .model_class()
            .objects.filter(content_type=plan_content_type)
            .filter(question__isnull=False)
            .order_by("-timestamp")
        )

class StudentMembershipPurchaseView(TemplateView):
    template_name = "membership/payment.html"
