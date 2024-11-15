from django.db import models

# Create your models here.


class Notification(models.Model):
    sender = models.ForeignKey(
        "users.Profile",
        related_name="notification_sender",
        on_delete=models.CASCADE,
    )
    receiver = models.ForeignKey(
        "users.Profile",
        related_name="notification_recipient",
        on_delete=models.CASCADE,
    )
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender} to {self.receiver}"


class Message(models.Model):
    sender = models.ForeignKey(
        "users.Profile", related_name="message_sender", on_delete=models.CASCADE,
    )
    receiver = models.ForeignKey(
        "users.Profile", related_name="message_recipient", on_delete=models.CASCADE,
    )
    title = models.CharField(max_length=255)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)


    def __str__(self):
        return f"{self.sender} to {self.receiver}: {self.title}"
