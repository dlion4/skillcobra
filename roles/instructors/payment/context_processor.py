from .forms import InstructorPayoutForm


def handle_instructor_payment_context(request):
    if request.user.is_authenticated:
        return {"payout_form": InstructorPayoutForm(profile=request.user.user_profile)}
    return {}
