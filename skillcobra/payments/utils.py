import random
import string


def generate_reference_id(length: int = 13):
    return "".join(
        random.choices(  # noqa: S311
            str(string.ascii_uppercase + string.digits), k=length,
        ),
    )
