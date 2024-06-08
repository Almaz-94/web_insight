from django.urls import path

from payment_youkassa.apps import PaymentYoukassaConfig
from payment_youkassa.views import PaymentView, PaymentSuccessView, WebhookView

app_name = PaymentYoukassaConfig.name
urlpatterns = [
    path('', PaymentView.as_view(), name='payment'),
    path('success/', PaymentSuccessView.as_view(), name='payment_success'),
    path('webhook/', WebhookView.as_view(), name='webhook'),
]