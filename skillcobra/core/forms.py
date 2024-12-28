from django import forms

from .models import Enrollment, Message as MessageModel, Review


class MessageForm(forms.ModelForm):
    class Meta:
        model = MessageModel
        fields = [
            "title",
            "content",
        ]
        widgets = {
            "title": forms.TextInput(
                attrs={
                    "placeholder": "Enter a title", "class": "form-control py-2",
                },
            ),
            "content": forms.Textarea(
                attrs={
                    "placeholder": "Enter your message",
                    "class": "form-control py-2",
                    "rows": 3,
                },
            ),
        }
        labels = {
            "title": "Message Title",
            "content": "Message content",
        }

    def __init__(self, *args, **kwargs):
        self.profile = kwargs.pop("profile", None)
        super().__init__(*args, **kwargs)


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = [
            "rating",
            "content",
        ]
        widgets = {
            "rating": forms.NumberInput(
                attrs={
                    "placeholder": "Rate the course (1-5)",
                    "class": "prompt srch_explore form-control",
                    "max_length":1,
                    "min": 1,
                    "max": 5,
                },
            ),
            "content": forms.Textarea(
                attrs={
                    "placeholder": "Enter your review",
                    "class": "form-control",
                    "rows": 3,
                },
            ),
        }
    def __init__(self, *args, **kwargs):
        self.profile = kwargs.pop("profile", None)
        super().__init__(*args, **kwargs)

class EnrollmentForm(forms.ModelForm):
    class Meta:
        model = Enrollment
        fields = [
            "email_address",
        ]
        widgets = {
            "email_address": forms.EmailInput(
                attrs={
                    "placeholder": "Enter your email address",
                    "class": "form-control",
                },
            ),
        }
    def __init__(self, *args, **kwargs):
        self.profile = kwargs.pop("profile", None)
        super().__init__(*args, **kwargs)
