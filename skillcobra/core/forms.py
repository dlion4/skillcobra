from django import forms

from .models import Message as MessageModel


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
