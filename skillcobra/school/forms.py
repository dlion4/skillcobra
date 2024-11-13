from django import forms
from django.forms import widgets
from django_ckeditor_5.widgets import CKEditor5Widget

from .models import COURSE_LEVEL_CHOICES, CourseCurriculum, Lecture
from .models import Category
from .models import Course
from .models import SubCategory


class GroupedChoiceField(forms.ChoiceField):
    def __init__(self, *args, **kwargs):
        categories = Category.objects.all()
        category_choices = []
        for category in categories:
            if category.get_all_subcategories().count() > 0:
                options = [
                    (
                        option.id,
                        option.name,
                    )
                    for option in category.get_all_subcategories()
                ]
                category_choices.append((category.name, options))
        kwargs["choices"] = category_choices
        super().__init__(*args, **kwargs)

    def clean(self, value):
        """Override the clean method to return a SubCategory instance"""
        try:
            return SubCategory.objects.get(id=value)
        except SubCategory.DoesNotExist as e:
            msg = f"Invalid subcategory selected. {e}"
            raise forms.ValidationError(msg) from e


class GroupedSelectWidget(widgets.Select):
    def __init__(self, *args, **kwargs):
        # Expecting 'sub_category' to be passed as 'groups' to the widget
        self.groups = kwargs.pop("sub_category", [])
        super().__init__(*args, **kwargs)

    def render(self, name, value, attrs=None, renderer=None):
        # Start by rendering the basic <select> element
        output = super().render(name, value, attrs, renderer)

        # If we have groups to render, we will modify the options within the <select>
        if self.groups:
            grouped_choices_html = ""
            for group, options in self.groups:
                grouped_choices_html += f'<optgroup label="{group}">'
                for option in options:
                    # Render each <option> element with its value and display name
                    grouped_choices_html += (
                        f'<option value="{option[0]}" '
                        f'{"selected" if option[0] == str(value) else ""}>{option[1]}</option>'
                    )
                grouped_choices_html += "</optgroup>"

            # The <select> tag is returned with its options grouped correctly
            return (
                f'<select title="{name}" name="{name}" class="{attrs.get("class", "")}" {attrs.get("data-live-search", "")}>'
                + grouped_choices_html
                + "</select>"
            )

        return output


class CourseForm(forms.ModelForm):
    sub_category = GroupedChoiceField(
        widget=GroupedSelectWidget(
            sub_category=[],  # The list of groups will be passed dynamically
            attrs={
                "class": "selectpicker",
                "data-live-search": "true",
            },
        ),
    )
    level = forms.ChoiceField(
        choices=COURSE_LEVEL_CHOICES,
        initial="beginner",
        widget=forms.Select(
            attrs={
                "class": "selectpicker",
                "title": "level",
            },
        ),
    )
    require_login = forms.BooleanField(
        initial=True,
        widget=forms.CheckboxInput(
            attrs={"class": "", "value": "on"},
        ),
    )
    require_enrollment = forms.BooleanField(
        initial=True,
        widget=forms.CheckboxInput(
            attrs={"class": ""},
        ),
    )
    regular_price = forms.DecimalField(
        required=False,
        initial="0.00",
        widget=forms.NumberInput(
            attrs={
                "class": "prompt srch_explore",
                "placeholder": "$0",
            },
        ),
    )
    discount_price = forms.DecimalField(
        required=False,
        initial="0.00",
        widget=forms.NumberInput(
            attrs={
                "class": "prompt srch_explore",
                "placeholder": "$0",
            },
        ),
    )

    class Meta:
        model = Course
        fields = [
            "title",
            "short_description",
            "course_description",
            "sub_category",
            "level",
            "require_login",
            "require_enrollment",
            "regular_price",
            "discount_price",
        ]

        widgets = {
            "title": forms.TextInput(attrs={"class": "prompt srch_explore"}),
            "short_description": CKEditor5Widget(
                config_name="minor_editor",
                attrs={
                    "class": "django_ckeditor_5",
                    "style": "height: 300px !important;",
                    "placeholder": "Just a short description about your course in 220 words",
                },
            ),
            "course_description": CKEditor5Widget(
                attrs={
                    "class": "django_ckeditor_5",
                    "style": "height: 300px !important;",
                    "placeholder": """
                    Explain in detail what your course is all about including but not limited to
                    course outline,
                    prerequisites,
                    course materials,
                    learning outcomes,
                    assessment methods,
                    """,
                },
            ),
        }
        help_text = {
            "title": "(Please make this a maximum of 100 characters and unique.)",
        }


class CourseCurriculumForm(forms.ModelForm):
    class Meta:
        model = CourseCurriculum
        fields = [
            "module_title",
            # "module_description",
        ]
        widgets = {
            "module_title": forms.TextInput(attrs={"class": "form_input_1"}),
            # "module_description": forms.Textarea(attrs={"rows": "3"}),
        }


class CreateCourseCurriculumLectureForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(
        attrs={"class": "form_input_1", "placeholder": "lecture title"}))
    description = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "placeholder": "Just a simple or overview of what the lecture is about",
                "rows": 3,
            },
        ),
    )
    has_free_preview = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput())
    lecture_video_url = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={"class": "form-control", "rows": 3}),
    )
    video_runtime_hours = forms.IntegerField(
        required=False,
        initial="00",
        widget=forms.NumberInput(attrs={"class": "form-control form_input_1"}),
    )
    video_runtime_minutes = forms.IntegerField(
        required=False,
        initial="00",
        widget=forms.NumberInput(attrs={"class": "form-control form_input_1"}),
    )
    video_runtime_seconds = forms.IntegerField(
        required=False,
        initial="00",
        widget=forms.NumberInput(attrs={"class": "form-control form_input_1"}),
    )
    lecture_attachments = forms.FileField(
        required=False,
        help_text="Upload your lecture attachments (e.g., PowerPoint, PDF, Word)",
        widget=forms.ClearableFileInput(
            attrs={
                "class": "form-control file-upload-input"}),
    )

    class Meta:
        model = Lecture
        fields = [
            "title",
            "description",
            "has_free_preview",
            "lecture_video_url",
            "video_runtime_hours",
            "video_runtime_minutes",
            "video_runtime_seconds",
            "lecture_attachments",
        ]