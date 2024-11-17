import contextlib

from django import forms
from django_countries.widgets import CountrySelectWidget

from skillcobra.payments.choices import PayoutAccountChoices
from skillcobra.payments.models import AirtelAccount
from skillcobra.payments.models import BankAccount
from skillcobra.payments.models import BillingAddress
from skillcobra.payments.models import MpesaAccount
from skillcobra.payments.models import PayoutAccount
from skillcobra.payments.models import PaypalAccount


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


class BillingAddressForm(forms.ModelForm):
    address_line2 = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "prompt srch_explore py-2",
                "id": "address_line2",
                "placeholder": "Address Line 2",
            },
        ),
    )

    class Meta:
        model = BillingAddress
        fields = [
            "first_name",
            "last_name",
            "country",
            "address_line1",
            "address_line2",
            "city",
            "state",
            "postal_code",
            "phone_number",
        ]
        widgets = {
            "first_name": forms.TextInput(
                attrs={
                    "class": "prompt srch_explore py-2",
                    "id": "firstName",
                    "placeholder": "John",
                },
            ),
            "last_name": forms.TextInput(
                attrs={
                    "class": "prompt srch_explore py-2",
                    "id": "lastName",
                    "placeholder": "Doe",
                },
            ),
            "country": CountrySelectWidget(),
            "address_line1": forms.TextInput(
                attrs={
                    "class": "prompt srch_explore py-2",
                    "id": "address_line1",
                    "placeholder": "Address Line 1",
                },
            ),
            "city": forms.TextInput(
                attrs={
                    "class": "prompt srch_explore py-2",
                    "id": "city",
                    "placeholder": "City",
                },
            ),
            "state": forms.TextInput(
                attrs={
                    "class": "prompt srch_explore py-2",
                    "id": "state",
                    "placeholder": "State",
                },
            ),
            "postal_code": forms.TextInput(
                attrs={
                    "class": "prompt srch_explore py-2",
                    "id": "postal_code",
                    "placeholder": "Postal Code",
                },
            ),
            "phone_number": forms.TextInput(
                attrs={
                    "class": "prompt srch_explore py-2",
                    "id": "phone_number",
                    "placeholder": "Phone number with country code",
                },
            ),
        }

    def __init__(self, *args, **kwargs):
        self.profile = kwargs.pop("profile", None)
        super().__init__(*args, **kwargs)
        if self.profile and hasattr(self.profile, "profile_billing_address"):
            billing_address = self.profile.profile_billing_address
            for field_name, field in self.fields.items():
                if hasattr(billing_address, field_name):
                    field.initial = getattr(billing_address, field_name)
        for field_name, field in self.fields.items():
            field.widget.attrs.update(
                {
                    "class": "prompt srch_explore py-3",
                    "id": f"{field_name}",
                },
            )
            if field_name == "country":
                field.widget.attrs.update({"class": "selectpicker"})


class BankPayoutAccountForm(forms.Form):
    account_number = forms.CharField(
        required=False,
        widget=forms.NumberInput(attrs={"class": "prompt srch_explore py-3"}),
    )
    account_name = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={"class": "prompt srch_explore py-3"}),
    )
    bank_name = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={"class": "prompt srch_explore py-3"}),
    )
    account_type = forms.CharField(
        initial=PayoutAccountChoices.BANK,
        widget=forms.HiddenInput(attrs={"id": "bank_account_type"}),
    )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user")
        super().__init__(*args, **kwargs)
        with contextlib.suppress(PayoutAccount.DoesNotExist, BankAccount.DoesNotExist):
            payout_account = PayoutAccount.objects.filter(
                owner=self.user.user_profile,
                account_type=PayoutAccountChoices.BANK,
            ).first()
            if bank_payout_account := BankAccount.objects.get(
                payout_account=payout_account,
            ):
                self.fields["account_number"].initial = (
                    bank_payout_account.account_number
                )
                self.fields["account_name"].initial = bank_payout_account.account_name
                self.fields["bank_name"].initial = bank_payout_account.bank_name


class PaypalPayoutAccountForm(forms.Form):
    email_address = forms.EmailField(
        required=False,
        widget=forms.EmailInput(
            attrs={
                "class": "prompt srch_explore py-2",
                "id": "emailAddress",
            },
        ),
    )
    account_type = forms.CharField(
        initial=PayoutAccountChoices.PAYPAL,
        widget=forms.HiddenInput(attrs={"id": "paypal_account_type"}),
    )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        with contextlib.suppress(
            PayoutAccount.DoesNotExist,
            PaypalAccount.DoesNotExist,
        ):
            if payout_account := PayoutAccount.objects.filter(
                owner=self.user.user_profile,
                account_type=PayoutAccountChoices.PAYPAL,
            ).first():
                account = PaypalAccount.objects.get(payout_account=payout_account)
                self.fields["email_address"].initial = account.email_address
            else:
                self.fields["email_address"].initial = self.user.email


class MpesaPayoutAccountForm(forms.Form):
    # Fields for Mpesa account
    phone_number = forms.CharField(
        required=False,
        widget=forms.NumberInput(
            attrs={
                "class": "prompt srch_explore py-2",
                "id": "mpesaPhoneNumber",
                "placeholder": "Phone number with country code",
            },
        ),
    )

    account_type = forms.CharField(
        initial=PayoutAccountChoices.MPESA,
        widget=forms.HiddenInput(attrs={"id": "mpesa_account_type"}),
    )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user")
        super().__init__(*args, **kwargs)
        with contextlib.suppress(PayoutAccount.DoesNotExist, MpesaAccount.DoesNotExist):
            if payout_account := PayoutAccount.objects.filter(
                owner=self.user.user_profile,
                account_type=PayoutAccountChoices.MPESA,
            ).first():
                account = MpesaAccount.objects.get(payout_account=payout_account)
                self.fields["phone_number"].initial = account.phone_number


class AirtelPayoutAccountForm(forms.Form):
    phone_number = forms.CharField(
        required=False,
        widget=forms.NumberInput(
            attrs={
                "class": "prompt srch_explore py-2",
                "id": "airtelPhoneNumber",
                "placeholder": "Phone number with country code",
            },
        ),
    )
    account_type = forms.CharField(
        initial=PayoutAccountChoices.AIRTEL,
        widget=forms.HiddenInput(attrs={"id": "airtel_account_type"}),
    )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user")
        super().__init__(*args, **kwargs)
        with contextlib.suppress(
            PayoutAccount.DoesNotExist,
            AirtelAccount.DoesNotExist,
        ):
            if payout_account := PayoutAccount.objects.filter(
                owner=self.user.user_profile,
                account_type=PayoutAccountChoices.AIRTEL,
            ).first():
                account = AirtelAccount.objects.get(payout_account=payout_account)
                self.fields["phone_number"].initial = account.phone_number


class PayoutAccountForm(forms.Form):
    # Fields for bank payout account
    account_number = forms.CharField(
        required=False,
        widget=forms.NumberInput(),
    )
    account_name = forms.CharField(
        required=False,
        widget=forms.TextInput(),
    )
    bank_name = forms.CharField(
        required=False,
        widget=forms.TextInput(),
    )

    # Fields for PayPal account
    email_address = forms.EmailField(
        required=False,
        widget=forms.EmailInput(),
    )

    # Fields for Mpesa account
    phone_number = forms.CharField(
        required=False,
        widget=forms.NumberInput(),
    )

    account_type = forms.CharField(widget=forms.HiddenInput())


class CreditDebitMembershipPaymentForm(forms.Form):
    card_holder_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "prompt srch_explore py-3",
                "id": "cardHolderName",
                "placeholder": "Card Holder's Name",
            },
        ),
    )
    card_number = forms.CharField(
        widget=forms.NumberInput(
            attrs={
                "class": "prompt srch_explore py-3",
                "id": "cardNumber",
                "placeholder": "Card Number",
            },
        ),
    )
    expiry_month = forms.ChoiceField(
        choices=tuple(
            zip(
                range(1, 13),
                [
                    "January",
                    "February",
                    "March",
                    "April",
                    "May",
                    "June",
                    "July",
                    "August",
                    "September",
                    "October",
                    "November",
                    "December",
                ],
                strict=False,
            ),
        ),
        widget=forms.Select(
            attrs={
                "class": "selectpicker",
            }
        ),
    )
    expiry_year = forms.CharField(
        widget=forms.NumberInput(
            attrs={
                "class": "prompt srch_explore py-3",
                "id": "expiryYear",
                "placeholder": "Expiry Year",
            },
        ),
    )
    card_cvv_number = forms.CharField(
        widget=forms.NumberInput(
            attrs={
                "class": "prompt srch_explore py-3",
                "id": "cardCvvNumber",
                "placeholder": "CVV",
            },
        ),
    )
    def __init__(self, *args, **kwargs):
        self.profile = kwargs.pop("profile")
        super().__init__(*args, **kwargs)
        with contextlib.suppress(Exception):
            captured = self.profile.profile_card_capture.first()
            for field_name, field in self.fields.items():
                if hasattr(captured, field_name):
                    field.initial = getattr(captured, field_name)
