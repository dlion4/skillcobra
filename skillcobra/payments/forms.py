import datetime as utcDate
import re
from datetime import datetime

from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone


class CoursePurchasePaymentForm(forms.Form):
    full_name = forms.CharField(
        label="Name on card",
        initial="Jeckonia Kwasa",
        widget=forms.TextInput(
            attrs={
                "class": "form-control py-2",
                "id": "cardName",
                "placeholder": "Your full name",
            },
        ),
    )

    card_number = forms.CharField(
        label="Card number",
        initial="5424000000000015",
        widget=forms.NumberInput(
            attrs={
                "class": "form-control py-2",
                "id": "cardNumber",
                "placeholder": "6566 5612 3456 7890",
            },
        ),
        required=True,
    )

    expiry_date = forms.CharField(
        label="Expiry Date (MM/YY)",
        initial="12/46",
        widget=forms.TextInput(
            attrs={
                "class": "form-control py-2",
                "id": "expiryDate",
                "placeholder": "MM/YY",
            },
        ),
        required=True,
    )

    cvv = forms.CharField(
        label="CVV",
        initial="243",
        widget=forms.NumberInput(
            attrs={"class": "form-control py-2", "id": "cvv", "placeholder": "***"},
        ),
        required=True,
    )
    coupon = forms.CharField(widget=forms.HiddenInput(), required=False)
    amount = forms.DecimalField(widget=forms.HiddenInput())
    courses_ids = forms.CharField(widget=forms.HiddenInput())
    def __init__(self, *args, **kwargs):
        self.profile = kwargs.pop("profile", None)
        super().__init__(*args, **kwargs)  # Call the parent class's
        if self.profile is not None:
            self.fields["full_name"].initial = self.profile.full_name().title()

    # def clean_expiry_date(self):
    #     expiry_date = self.cleaned_data["expiry_date"]
    #     if not re.match(r"^(0[1-9]|1[0-2])\/?([0-9]{2})$", expiry_date):
    #         msg = "Expiry date must be in MM/YY format."
    #         raise ValidationError(msg)
    #     month, year = map(int, expiry_date.split("/"))
    #     expiry_datetime = datetime(
    #         year + 2000, month, tzinfo=utcDate.UTC,
    #     )
    #     expiry_datetime = expiry_datetime.replace(
    #         day=1,
    #     )
    #     current_datetime = timezone.now()
    #     if expiry_datetime < current_datetime:
    #         msg = "The expiry date cannot be in the past."
    #         raise ValidationError(msg)

    #     return expiry_date
