"""
            transaction_response = res.get("createTransactionResponse").get(
            "transactionResponse",
        )
        if (
            res.get("createTransactionResponse").get("messages").get("resultCode")
            == "Error"
        ):
            error_message = (
                transaction_response.get("errors").get("error").get("errorText")
            )
            return JsonResponse({"detail": error_message}, status=400)
        if (
            res.get("createTransactionResponse").get("messages").get("resultCode")
            == "Ok"
        ):
            success_message = (
                transaction_response.get("messages").get("message").get("description")
            )
            money_data = res.get("createTransactionResponse").get("amount")
            for pk in json.loads(data.get("courses_ids", None)):
                course = Course.objects.get(pk=int(pk))
                payment_details = {
                    "amount": str(money_data.get("value")),
                    "currency": str(money_data.get("currency")),
                    "account_type": transaction_response.get("accountType"),
                    "payment_reference": str(str(
                        res.get("createTransactionResponse").get("refId"),
                    ) + f"_{time.time()}"),
                }
                self._create_payment_success_transaction(
                    student=profile,
                    parent=course,
                    payment_details=payment_details,
                )

    """
