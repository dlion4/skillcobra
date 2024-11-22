from skillcobra.core.forms import EnrollmentForm


def core_context_processor(request):
    """"""
    # Add your custom context variables here
    user = request.user
    if user.is_authenticated:
        return {
            "enrolment_form": EnrollmentForm(profile=user.user_profile),
        }
    return {}
