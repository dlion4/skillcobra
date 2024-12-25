import random
import string

import requests
from django.conf import settings
from django.http import JsonResponse


def generate_reference_id(length: int = 13):
    return "".join(
        random.choices(  # noqa: S311
            str(string.ascii_uppercase + string.digits), k=length,
        ),
    )

def cleaned_transaction_response(response):
    transaction_response = response.get("createTransactionResponse").get(
        "transactionResponse",
    )
    if (
        response.get("createTransactionResponse").get("messages").get("resultCode")
        == "Error"
    ):
        error_message = (
            transaction_response.get("errors").get("error").get("errorText")
        )
        return JsonResponse({"detail": error_message}, status=400)
    return transaction_response

def handle_payment_processing_view(data, profile):
    expiry_date = data.pop("expiry_date")
    month, year = tuple(expiry_date.split("/"))
    payment_upload_data = {
        "cardNumber": data.get("card_number"),
        "expirationDate": f"20{year}-{month}",
        "cardCode": data.get("cvv"),
        "invoiceNumber": generate_reference_id(11),
        "description": "course purchase",
        "itemId": "22",
        "itemDescription": "This is purchase for course",
        "itemTotalPrice": str(data.get("amount")),
        "customer_email": str(profile.user.email),
    }

    response = requests.post(
        f"{settings.SYNCPAY_MERCHANT_PAYMENT_URL!s}/api/v1/payments/developers/process-payment/",
        json=payment_upload_data,
        timeout=10,
        headers={
            "Authorization": "Bearer OwTsvQoaRiTIW2UwS8BFrEVnn00sGgSGfBCiPc1735060072",
        },
    )
    response.raise_for_status()
    return response.json()

