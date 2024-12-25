from django import forms

from roles.instructors.payment.models import InstructorPayout
from skillcobra.payments.models import PayoutAccount


class InstructorPayoutForm(forms.ModelForm):
    amount = forms.DecimalField(
        max_digits=12,
        decimal_places=2,
        initial=0.00,
        widget=forms.NumberInput(
            attrs={
                "class": "prompt srch_explore form-control py-2",
                "hx-url": "/instructor/payments/balance-lookup/",
            },
        ),
    )
    channel = forms.ModelChoiceField(
        queryset=PayoutAccount.objects.all(),
        initial="Select Payment Channel",
        widget=forms.Select(
            attrs={"class": "form-control form-select py-2"},
        ),
    )

    class Meta:
        model = InstructorPayout
        fields = ["amount", "channel"]

    def __init__(self, *args, **kwargs):
        self.profile = kwargs.pop("profile", None)
        super().__init__(*args, **kwargs)
        self.fields["channel"].queryset = PayoutAccount.objects.filter(
            owner=self.profile,
        ).distinct("account_type")
    class Media:
        js = ["js/instructors.js"]
