from django.contrib.auth import get_user
from django.shortcuts import get_object_or_404

from roles.instructors.instructor.views import TemplateViewMixin
from skillcobra.core.forms import MessageForm
from skillcobra.school.forms import DiscussionForm
from skillcobra.school.forms import DiscussionReplyForm
from skillcobra.users.models import Profile


class InstructorTemplateViewMixin(TemplateViewMixin):
    def get_template_names(self):
        return [f"instructors/{self.template_name}"]

    def get_profile(self):
        return self.get_object()

    def get_object(self):
        return get_object_or_404(
            Profile,
            pk=self.kwargs.get("pk"),
            user__username=self.kwargs.get("username"),
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["instructor"] = self.get_profile()
        return context


class InstructorProfileView(InstructorTemplateViewMixin):
    template_name = "instructor_profile.html"
    discussion_form = DiscussionForm
    discussion_reply_form = DiscussionReplyForm
    message_form = MessageForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["discussions"] = self.get_profile().get_discussions()
        context["discussion_form"] = self.discussion_form()
        context["discussion_reply_form"] = self.discussion_reply_form()
        context["instructor_subscription_ids"] = list(
            self.get_profile().tutor_subscriptions.students.values_list("pk", flat=True)
        )
        context["profile"] = get_user(self.request).user_profile
        context["message_form"] = self.message_form(profile=context["profile"])
        context[
            "student_purchased_courses"
        ] = self.get_profile().purchased_courses.filter(
            tutor=Profile.objects.get(
                pk=kwargs.get("pk"),
            ),
        )
        return context
