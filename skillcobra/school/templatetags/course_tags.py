from django import template
from django.db.models import QuerySet

from skillcobra.school.models import SavedCourse

register = template.Library()

@register.filter
def is_saved(obj, profile):
    # print(SavedCourse.objects.all())
    if isinstance(profile.get_saved_courses(), QuerySet):
        return obj.pk in profile.get_saved_courses().values_list("pk", flat=True)
    return obj.pk in profile.get_saved_courses()
