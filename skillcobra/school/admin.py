from django.contrib import admin

# Register your models here.
from unfold.admin import ModelAdmin
from unfold.admin import StackedInline
from unfold.widgets import AdminTextareaWidget

from .models import Category
from .models import Course
from .models import CourseCurriculum
from .models import Discussion, DiscussionReply
from .models import Lecture
from .models import SubCategory


class SubCategoryInline(StackedInline):
    model = SubCategory
    extra = 0


@admin.register(Category)
class CategoryAdmin(ModelAdmin):
    inlines = [SubCategoryInline]


class LectureInline(StackedInline):
    model = Lecture
    extra = 0


@admin.register(CourseCurriculum)
class CourseCurriculumAdmin(ModelAdmin):
    inlines = [LectureInline]


class CourseCurriculumInline(StackedInline):
    model = CourseCurriculum
    extra = 0


@admin.register(Course)
class CourseModelAdmin(ModelAdmin):
    list_display = [
        "tutor",
        "course_duration",
        "level",
        "is_free_course",
        "require_login",
        "require_enrollment",
        "regular_price",
        "discount_price",
        "payable_amount",
        "allow_student_submission",
        "updated_at",
        "status",
        "views",
        "likes",
        "un_likes",
        "paid",
        "balance",
    ]
    actions = ["approve_course", "disapprove_course"]
    inlines = [CourseCurriculumInline]

    @admin.action(description="Approve Course")
    def approve_course(self, request, queryset):
        queryset.update(status="approved")

    @admin.action(description="Disapprove Course")
    def disapprove_course(self, request, queryset):
        queryset.update(status="draft")

    def get_queryset(self, request):
        return self.model.all_objects.all()


class DiscussionReplyInlineModel(StackedInline):
    model = DiscussionReply
    extra = 0


@admin.register(Discussion)
class DiscussionAdmin(ModelAdmin):
    inlines = [DiscussionReplyInlineModel]

    def get_queryset(self, request):
        return self.model.all_objects().all()
