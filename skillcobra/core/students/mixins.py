import logging
from functools import wraps

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.shortcuts import get_object_or_404

from skillcobra.school.models import Course
from skillcobra.school.models import SavedCourse

logger = logging.getLogger(__name__)


class RetrieveCourseMixin:
    @staticmethod
    def course_wrapper(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            course = get_object_or_404(
                Course,
                pk=kwargs.get("course_pk"),
                slug=kwargs.get("course_slug"),
            )
            request.course = course
            request.student = request.user.user_profile
            return view_func(request, *args, **kwargs)

        return wrapper


class AuthenticatedRetrieveCourseMixin(LoginRequiredMixin, RetrieveCourseMixin):
    @classmethod
    def as_view(cls, **initkwargs):
        view = super().as_view(**initkwargs)
        return cls.course_wrapper(view)


class LikeCourseViewMixin(AuthenticatedRetrieveCourseMixin):
    @classmethod
    def as_view(cls, **initkwargs):
        view = super().as_view(**initkwargs)

        @wraps(view)
        def wrapper(request, *args, **kwargs):
            response = view(request, *args, **kwargs)
            course = getattr(request, "course", None)
            student = getattr(request, "user", None)
            if not course or not student:
                return response
            logger.info(
                f"Course tutor: {course.tutor}, created at: {course.created_at}",  # noqa: G004
            )
            try:
                with transaction.atomic():
                    liked_course, _ = SavedCourse.objects.get_or_create(
                        student=student.user_profile,
                    )
                    if course.pk not in liked_course.courses.values_list(
                        "pk",
                        flat=True,
                    ):
                        liked_course.courses.add(course)
                        print(liked_course.courses.values("pk"))
                        print(course.pk)
                        logger.info(
                            f"Course {course.pk} added to liked courses for student {student.pk}",  # noqa: G004
                        )
                    else:
                        logger.info(
                            f"Course {course.pk} already in liked courses for student {student.pk}",  # noqa: E501
                        )
            except Exception as e:
                logger.exception(f"Error saving liked course: {e}")  # noqa: TRY401
                raise ValueError(e) from e
            return response
        return wrapper

class UnLikeCourseViewMixin(AuthenticatedRetrieveCourseMixin):
    @classmethod
    def as_view(cls, **initkwargs):
        view = super().as_view(**initkwargs)
        @wraps(view)
        def wrapper(request, *args, **kwargs):
            response = view(request, *args, **kwargs)
            course = getattr(request, "course", None)
            student = getattr(request, "user", None)
            if course and student:
                cls.remove_course_from_liked_courses(course, student)
            return response
        return wrapper
    @staticmethod
    @transaction.atomic()
    def remove_course_from_liked_courses(course, student):
        try:
            saved_course = SavedCourse.objects.get(student=student.user_profile)
            if course in saved_course.courses.all():
                saved_course.courses.remove(course)
        except ObjectDoesNotExist as e:
            msg = "No saved course found for student"
            raise ValueError(msg) from e
        except Exception as e:
            raise ValueError(str(e)) from e
