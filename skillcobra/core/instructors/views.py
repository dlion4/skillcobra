from django.contrib.auth import get_user
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from roles.instructors.instructor.views import TemplateViewMixin
from skillcobra.core.forms import MessageForm
from skillcobra.core.forms import ReviewForm
from skillcobra.core.models import Review
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
            username=self.kwargs.get("username"),
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["instructor"] = self.get_profile()
        return context

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        if request.user.role not in ["instructor", "student"]:
            return redirect("home")
        return super().dispatch(request, *args, **kwargs)


class InstructorProfileView(InstructorTemplateViewMixin):
    template_name = "instructor_profile.html"
    discussion_form = DiscussionForm
    discussion_reply_form = DiscussionReplyForm
    message_form = MessageForm
    review_form = ReviewForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["discussions"] = self.get_profile().get_discussions()
        context["discussion_form"] = self.discussion_form()
        context["discussion_reply_form"] = self.discussion_reply_form()
        context["instructor_subscription_ids"] = list(
            self.get_profile().get_subscribed_tutor_ids(),
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
        context["review_form"] = self.review_form(
            profile=self.request.user.user_profile
        )
        content_type = ContentType.objects.get_for_model(self.get_profile())
        context["reviews"] = Review.objects.filter(
            content_type=content_type, object_id=content_type.pk
        )
        context["review_ratting_range"] = range(1, 6)
        return context
    def post(self, request, *args, **kwargs):
        if request.POST.get("form_name") == "review_tutor":
            return self._handle_tutor_review(request, *args, **kwargs)
        return JsonResponse({}, status=200)

    def self_handle_tutor_review(self, request, *args, **kwargs):
        reviewer = request.user.user_profile
        review_form = self.review_form(request.POST, profile=reviewer)
        try:
            tutor = get_object_or_404(
                Profile,
                pk=kwargs.get("pk"),
                username=kwargs.get("username"),
                user__role="instructor",
            )
            if review_form.is_valid():
                review = review_form.save(commit=False)
                review.content_object = ContentType.objects.get_for_model(tutor)
                review.save()
                return render(
                    request,
                    "instructors/components/reviews/tutor.html",
                    {"review": review},
                )
            return JsonResponse({"message": "Invalid form data."}, status=400)
        except (Profile.DoesNotExist, Exception) as e:
            return JsonResponse({"message": str(e)}, status=400)
