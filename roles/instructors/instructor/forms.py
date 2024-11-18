from django import forms
from froala_editor.widgets import FroalaEditor

from roles.instructors.instructor.models import ScheduleClass
from skillcobra.school.models import Course


class ScheduleClassForm(forms.ModelForm):
    courses = forms.ModelChoiceField(
        queryset=Course.objects.none(),
        widget=forms.Select(attrs={"class": "selectpicker"}),
    )
    lesson_overview = forms.CharField(
        initial="<h2>Lesson Overview</h2><br />",
        widget=FroalaEditor(),
    )
    class Meta:
        model = ScheduleClass
        fields = [
            "courses",
            "lesson_overview",
            "class_start_time",
            "class_end_time",
        ]
        widgets = {
            "class_start_time": forms.DateTimeInput(
                attrs={"class": "_dlor1 prompt srch_explore py-2", "required": True},
            ),
            "class_end_time": forms.DateTimeInput(
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
