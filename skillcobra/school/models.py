import re
from datetime import datetime
from datetime import timedelta

from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify
from django_ckeditor_5.fields import CKEditor5Field

from skillcobra.school.utils import upload_lecture_attachment

COURSE_LEVEL_CHOICES = [
    ("beginner", "Beginner"),
    ("intermediate", "Intermediate"),
    ("expert", "Expert"),
]


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.name

    def get_all_subcategories(self):
        return self.subcategories.all()


class SubCategory(models.Model):
    category = models.ForeignKey(
        "Category",
        on_delete=models.CASCADE,
        related_name="subcategories",
    )
    name = models.CharField(max_length=255)
    value = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"{self.category.name} - {self.name}"

    def save(self, *args, **kwargs):
        self.name = self.name.title()
        self.value = self.name
        super().save(*args, **kwargs)


class Course(models.Model):
    tutor = models.ForeignKey(
        "users.Profile", on_delete=models.DO_NOTHING, related_name="course_tutor"
    )
    sub_category = models.ForeignKey(
        SubCategory,
        on_delete=models.DO_NOTHING,
        related_name="course_category_subcategory",
        blank=True,
        null=True,
    )
    title = models.CharField(
        help_text="Please make this a maximum of 100 characters and unique",
        max_length=200,
    )
    slug = models.SlugField(
        help_text="Please make this a maximum of 100 characters and unique",
    )
    short_description = CKEditor5Field(
        config_name="minor_editor",
        help_text="Please make this a maximum of 220 words",
        max_length=5000,
    )
    course_description = CKEditor5Field(
        help_text="Please make this a maximum of 5000 words"
    )

    level = models.CharField(
        choices=COURSE_LEVEL_CHOICES,
        help_text="Please select the level of this course",
        max_length=100,
        default="beginner",
    )

    is_free_course = models.BooleanField(default=False)
    require_login = models.BooleanField(default=True)
    require_enrollment = models.BooleanField(default=True)

    regular_price = models.DecimalField(
        help_text="Please enter a valid decimal number",
        max_digits=12,
        decimal_places=2,
        default=0.00,
    )
    discount_price = models.DecimalField(
        help_text="Please enter a valid decimal number",
        max_digits=12,
        decimal_places=2,
        default=0.00,
    )

    allow_student_submission = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=100,
        choices=[
            ("draft", "Draft"),
            ("approved", "Approved"),
        ],
        default="draft",
    )

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse(
            "instructors:detail_course_view",
            kwargs={
                "pk": self.pk,
                "slug": self.slug,
            },
        )

    def is_new_course(self):
        return self.created_at >= (datetime.now(tz=timezone.UTC) - timedelta(days=7))

    def get_course_modules(self):
        return self.course_curriculum.all()


class CourseCurriculum(models.Model):
    course = models.ForeignKey(
        Course,
        on_delete=models.DO_NOTHING,
        related_name="course_curriculum",
    )
    tutor = models.ForeignKey(
        "users.Profile",
        on_delete=models.DO_NOTHING,
        related_name="course_curriculum_profile",
    )
    module_title = models.CharField(max_length=100)
    module_slug = models.SlugField(max_length=100)
    module_description = models.TextField(
        max_length=5000,
        help_text="Please make this a maximum of 5000 words",
        blank=True,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["course", "tutor", "module_title"],
                name="unique_course_title",
            ),
        ]

    def __str__(self):
        return self.module_title

    def save(self, *args, **kwargs):
        if not self.module_slug:
            self.module_slug = slugify(self.module_title)
        super().save(*args, **kwargs)

    def get_delete_url(self, *args, **kwargs):
        return reverse(
            "school:delete_course_module_view",
            kwargs={
                "module_pk": self.pk,
            },
        )

    def get_update_url(self, *args, **kwargs):
        return reverse(
            "school:update_course_module_view",
            kwargs={
                "module_pk": self.pk,
            },
        )

    def get_create_module_lecture(self):
        return reverse(
            "school:create_course_module_view",
            kwargs={
                "module_pk": self.pk,
            },
        )

    def get_all_curriculum_lectures(self):
        return self.course_module_lecture.all()


class Lecture(models.Model):
    module_lecture = models.ForeignKey(
        CourseCurriculum,
        on_delete=models.CASCADE,
        related_name="course_module_lecture",
    )
    title = models.CharField(
        max_length=100,
    )
    description = CKEditor5Field(
        config_name="minor_editor",
        help_text="Please make this a maximum of 220 words",
        max_length=5000,
        blank=True,
    )
    has_free_preview = models.BooleanField(default=True)
    lecture_video_url = models.TextField(
        help_text="""
        Please enter a valid video link or embedded URL or
        live blank if no video is available""",
        blank=True,
    )
    video_runtime_hours = models.IntegerField(default=0)
    video_runtime_minutes = models.IntegerField(default=0)
    video_runtime_seconds = models.IntegerField(default=0)
    lecture_attachments = models.FileField(
        blank=True, null=True, upload_to=upload_lecture_attachment
    )

    def __str__(self):
        return self.title

    def get_lecture_update_url(self):
        return reverse(
            "school:update_lecture_view",
            kwargs={
                "module_pk": self.module_lecture.pk,
                "lecture_pk": self.pk,
            },
        )
