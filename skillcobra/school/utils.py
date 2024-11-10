from time import time

from django.utils.timezone import now


def upload_lecture_attachment(instance, filename):
    """
    This function is used to handle the file upload for lecture attachments.
    It ensures that the file is saved with a unique name and moves it
    to the specified directory.
    """
    # Generate a unique filename by appending a timestamp to the original filename
    timestamp = int(time())
    return f"{now().year}/{now().month}/{now().day}/{instance.module_lecture.module_slug}/{timestamp}_{filename}"  # noqa: E501
