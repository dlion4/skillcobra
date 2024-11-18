from django import forms
from froala_editor.widgets import FroalaEditor

from roles.instructors.instructor.models import ScheduleClass
from skillcobra.school.models import Course


class ScheduleClassForm(forms.ModelForm):
    courses = forms.ModelChoiceField(
        queryset=Course.objects.none(),
        widget=forms.Select(attrs={"class": "selectpicker"}),
    )
    credentials = forms.CharField(
        initial="credentials: <br />",
        widget=FroalaEditor(),
    )
    login_required = forms.BooleanField(
        label="Require login credentials",
        required=False,
        initial=False,
        widget=forms.CheckboxInput(),
    )
    class Meta:
        model = ScheduleClass
        fields = [
            "courses",
            "class_live_link",
            "login_required",
            "credentials",
            "class_time",
        ]
        widgets = {
            "class_live_link": forms.TextInput(
                attrs={
                    "class": "_dlor1 prompt srch_explore py-2",
                    "placeholder": "https://stream.live.skillcobra.com/lessons",
                    "required": True,
                },
            ),
            "class_time": forms.DateTimeInput(
                attrs={"class": "_dlor1 prompt srch_explore py-2", "required": True},
            ),
        }
    def __init__(self, *args, **kwargs):
        self.profile = kwargs.pop("profile", None)
        super().__init__(*args, **kwargs)
        if self.profile:
            self.fields["courses"].queryset = Course.objects.filter(
                tutor=self.profile,
            )
            self.fields["class_live_link"].initial = (
                "https://stream.live.skillcobra.com/lessons"
            )
