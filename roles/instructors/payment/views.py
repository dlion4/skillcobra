from decimal import Decimal

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET
from django.views.decorators.http import require_POST

from roles.instructors.instructor.models import Account

from .forms import InstructorPayoutForm
from .models import InstructorPayout


@login_required
@csrf_exempt
@require_POST
def initiate_payout_view(request):
    form = InstructorPayoutForm(request.POST, profile=request.user.user_profile)
    account = Account.objects.get(holder=request.user.user_profile)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.instructor = request.user.user_profile
        instance.save()
        form.save()
        account.account_balance -= instance.amount
        account.save()
        return JsonResponse(
            {"message": "Payment Request sent. Will communicate in a few minutes"},
            status=200,
        )
    return JsonResponse(
        {"message": "Could not process your request at the moment. Try again later"},
        status=400,
    )


@login_required
@csrf_exempt
@require_GET
def account_balance_lookup_view(request):
    amount = Decimal(request.GET.get("amount", "0.00"))
    try:
        account = Account.objects.get(holder=request.user.user_profile)
        if amount > account.account_balance:
            return JsonResponse({"enough": False}, status=200)
        return JsonResponse({"enough": True}, status=200)
    except Account.DoesNotExist:
        return JsonResponse({"enough": False}, status=404)
