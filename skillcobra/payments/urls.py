from django.urls import path

from .views import ProcessPaymentFormView

app_name = "payments"
urlpatterns = [path("process/", ProcessPaymentFormView.as_view(), name="pay")]
