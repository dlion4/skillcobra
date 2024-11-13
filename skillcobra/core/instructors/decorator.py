from functools import wraps

from django.contrib.auth import get_user
from django.shortcuts import get_object_or_404

from skillcobra.school.models import Discussion


def discussion_wrapper(func):
    @wraps(func)
    def wrapper(request, discussion_pk=None):
        request.student = get_user(request).user_profile
        discussion = get_object_or_404(
            Discussion,
            pk=discussion_pk,
        )
        request.discussion = discussion
        return func(request, discussion_pk)
    return wrapper
