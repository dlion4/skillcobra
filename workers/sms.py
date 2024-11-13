from django.utils.decorators import method_decorator
from django.views.generic import View
from django_twilio.decorators import twilio_view
from twilio.twiml.messaging_response import MessagingResponse


class ThanksView(View):

    @method_decorator(twilio_view)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request):
        r = MessagingResponse()
        r.message("Thanks for the SMS message!")
        return r
