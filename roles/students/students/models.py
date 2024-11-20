from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class Attendance(models.Model):
    student = models.OneToOneField(
        "users.Profile",
        on_delete=models.CASCADE,
        verbose_name=_("Student"),
        related_name="student_attendance",
    )
    course = models.OneToOneField(
        "school.Course",
        on_delete=models.CASCADE,
        verbose_name=_("Course"),
        related_name="course_attendance",
    )
    attendance_date = models.DateField(_("Attendance Date"), auto_now_add=True)
    present = models.BooleanField(_("Present"), default=True)
    attendance_counter = models.IntegerField(_("Attendance Counter"), default=1)
    notes = models.TextField(_("Notes"),blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    class Meta:
        verbose_name = _("Course Attendance")
        verbose_name_plural = _("Course Attendances")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("Attendance_detail", kwargs={"pk": self.pk})
