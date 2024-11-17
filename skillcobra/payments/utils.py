import random
import string

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
