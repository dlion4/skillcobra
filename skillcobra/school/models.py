from datetime import timedelta
from decimal import Decimal

from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify
from django_ckeditor_5.fields import CKEditor5Field
from froala_editor.fields import FroalaField

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


class CourseManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status="approved")


class Course(models.Model):
    tutor = models.ForeignKey(
        "users.Profile",
        on_delete=models.SET_NULL,
        related_name="course_tutor",
        blank=True,
        null=True,
    )
    cover = models.ImageField(upload_to="course/cover/", blank=True, null=True)
    course_duration = models.CharField(
        max_length=300,
        default="1 hour 3 minutes",
        help_text="Approximate duration of the course. Can be in weeks, days or even hours",
    )
    sub_category = models.ForeignKey(
        SubCategory,
        on_delete=models.CASCADE,
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
    short_description = models.CharField(
        help_text="Please make this a maximum of 220 words",
        max_length=5000,
    )
    course_description = FroalaField(
        help_text="Please make this a maximum of 5000 words",
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
    preview_video = models.URLField(max_length=500, blank=True)
    views = models.IntegerField(default=1)
    likes = models.IntegerField(default=1)
    un_likes = models.IntegerField(default=0)
    shared = models.IntegerField(default=11)

    all_objects = models.Manager()
    objects = CourseManager()

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

    def get_public_absolute_url(self):
        return reverse(
            "courses:course_detail_view",
            kwargs={
                "pk": self.pk,
                "slug": self.slug,
            },
        )

    def get_sales(self):
        return {"count": 21}

    @property
    def payable_amount(self):
        return Decimal(self.regular_price - self.discount_price)

    def get_delete_url(self):
        return reverse(
            "school:delete_course_view",
            kwargs={
                "course_pk": self.pk,
                "course_slug": self.slug,
            },
        )

    def is_new_course(self):
        return self.created_at >= (timezone.now() - timedelta(days=7))

    def get_course_modules(self):
        return self.course_curriculum.all()

    def get_course_curriculums(self):
        return self.course_curriculum.all()

    def get_cumulated_lectures(self):
        return Lecture.objects.filter(module_lecture__course=self)

    def _object_url(self, path: str, **extra_kwargs):
        kwargs = {
            "course_pk": self.pk,
            "course_slug": self.slug or slugify(self.title),
        } | extra_kwargs
        return reverse(path, kwargs=kwargs)

    def get_like_endpoint(self):
        return self._object_url("courses:course_like_view")

    def get_course_save_url(self):
        return self._object_url("profile_students:course_save_view")

    def get_course_unsave_url(self):
        return self._object_url("profile_students:course_unsave_view")

    def get_unlike_endpoint(self):
        return self._object_url("courses:course_unlike_view")

    def get_add_to_cart_url(self):
        return self._object_url("courses:add_course_to_cart")

    def get_remove_from_cart_url(self):
        return self._object_url("courses:remove_course_from_cart")


class CourseCurriculum(models.Model):
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="course_curriculum",
    )
    tutor = models.ForeignKey(
        "users.Profile",
        on_delete=models.CASCADE,
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
    description = FroalaField(
        help_text="Please make this a maximum of 220 words",
        max_length=5000,
        blank=True,
    )
    has_free_preview = models.BooleanField(default=False)
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
        blank=True,
        null=True,
        upload_to=upload_lecture_attachment,
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

    def get_lecture_delete_url(self):
        return reverse(
            "school:delete_lecture_view",
            kwargs={
                "module_pk": self.module_lecture.pk,
                "lecture_pk": self.pk,
            },
        )


class DiscussionManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)


class Discussion(models.Model):
    tutor = models.ForeignKey(
        "users.Profile",
        on_delete=models.CASCADE,
        related_name="tutor_discussion_profile",
    )
    student = models.ForeignKey(
        "users.Profile",
        on_delete=models.CASCADE,
        related_name="student_discussion",
    )
    message = models.CharField(max_length=3000)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    resolved = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    all_objects = models.Manager()
    objects = DiscussionManager()

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return "Discussion"

    def get_delete_url(self):
        return reverse(
            "profile_instructors:delete_discussion_view",
            kwargs={
                "discussion_pk": self.pk,
            },
        )

    def get_discussion_replies(self):
        return self.discussion_replies.all()


class DiscussionReply(models.Model):
    discussion = models.ForeignKey(
        Discussion,
        on_delete=models.CASCADE,
        related_name="discussion_replies",
    )
    profile = models.ForeignKey(
        "users.Profile",
        on_delete=models.CASCADE,
        related_name="discussion_replies_profile",
    )
    message = models.CharField(max_length=3000)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    resolved = models.BooleanField(default=False)

    def __str__(self):
        return "Reply"


class Subscription(models.Model):
    tutor = models.OneToOneField(
        "users.Profile",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="tutor_subscriptions",
    )
    students = models.ManyToManyField(
        "users.Profile",
        related_name="student_subscriptions",
        through="CourseSubscription",
    )

    def __str__(self):
        return ""


class CourseSubscription(models.Model):
    subscription = models.ForeignKey(
        Subscription, on_delete=models.SET_NULL, blank=True, null=True,
    )
    student = models.ForeignKey(
        "users.Profile", on_delete=models.SET_NULL, blank=True, null=True,
    )
    course = models.ForeignKey(
        "school.Course", on_delete=models.SET_NULL, blank=True, null=True,
    )
    date_subscribed = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.student} - {self.course}"


class SavedCourse(models.Model):
    student = models.OneToOneField(
        "users.Profile",
        on_delete=models.CASCADE,
        related_name="student_saved_course",
    )
    courses = models.ManyToManyField(Course, related_name="saved_courses")
    saved_date = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = "Saved Course"
        verbose_name_plural = "Saved Courses"
        ordering = ["-saved_date"]

    def __str__(self):
        return f"{self.student} saved {self.courses.count()} courses"


class CourseEnrollment(models.Model):

    def __str__(self):
        return ""


class CourseModuleProgress(models.Model):
    def __str__(self):
        return ""


class CourseModuleCompletion(models.Model):
    def __str__(self):
        return ""


class CourseLectureProgress(models.Model):
    def __str__(self):
        return ""


class CourseLectureCompletion(models.Model):
    def __str__(self):
        return ""


class CourseModuleAssessment(models.Model):
    def __str__(self):
        return ""
