import random
import string

from django.db import models


def generate_reference_id(instance: type[models.Model], length: int = 13):
    return "".join(
        random.choices(  # noqa: S311
            str(string.ascii_uppercase + string.digits + instance.pk), k=length,
        ),
    )
