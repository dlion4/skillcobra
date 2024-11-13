from django.conf import settings
from twilio.rest import Client


class TwilioMessageClient:
    def __init__(self):
        self.account_sid = settings.TWILIO_ACCOUNT_SID
        self.auth_token = settings.TWILIO_AUTH_TOKEN
    def post(self, request, *args, **kwargs):
        data = kwargs.get("message", "")
        recipients = kwargs.get("recipients",["+254745547755"])
        if isinstance(recipients, list):
            for recipient in recipients:
                return self.compose_message(data, recipient)
        return self.compose_message(data, recipients)
    def compose_message(self, data, _to):
        message = self._client.message.create(
            body=data,
            from_=str(settings.TWILIO_ACCOUNT_PHONE_NUMBER),
            to=_to,
        )
        return {"message_id": message.sid}
    def _client(self):
        return Client(self.account_sid, self.auth_token)
