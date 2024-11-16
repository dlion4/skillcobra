from skillcobra.payments.forms import AirtelPayoutAccountForm
from skillcobra.payments.forms import BankPayoutAccountForm
from skillcobra.payments.forms import MpesaPayoutAccountForm
from skillcobra.payments.forms import PaypalPayoutAccountForm


def payment_context_processor(request):
    return {
        "bank_payout_form":BankPayoutAccountForm(user=request.user),
        "paypal_payout_form":PaypalPayoutAccountForm(user=request.user),
        "mpesa_payout_form":MpesaPayoutAccountForm(user=request.user),
        "airtel_payout_form":AirtelPayoutAccountForm(user=request.user),
    }
