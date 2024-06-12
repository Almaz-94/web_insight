import json
import logging

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.conf import settings
from django.urls import reverse_lazy
from django.views import View
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views.generic import FormView, TemplateView

from yookassa import Configuration, Payment as YouKassaPayment
from yookassa.domain.notification import WebhookNotification

from users.models import User
from .forms import PaymentForm
from .models import Payment


Configuration.account_id = settings.YOUKASSA_SHOP_ID
Configuration.secret_key = settings.YOUKASSA_SECRET_KEY

class PaymentView(LoginRequiredMixin, FormView):
    template_name = 'payment_youkassa/payment_form.html'
    form_class = PaymentForm
    success_url = reverse_lazy('payment:payment_success')

    def form_valid(self, form):
        amount = form.cleaned_data['amount']
        youkassa_payment = YouKassaPayment.create({
            "amount": {
                "value": str(amount),
                "currency": "RUB"
            },
            "confirmation": {
                "type": "redirect",
                "return_url": self.request.build_absolute_uri(self.get_success_url())
            },
            "capture": True,
            "description": "Payment for order"
        })

        Payment.objects.create(
            user=self.request.user if self.request.user.is_authenticated else None,
            amount=amount,
            status='pending',
            payment_id=youkassa_payment.id
        )

        confirmation_url = youkassa_payment.confirmation.confirmation_url
        return redirect(confirmation_url)

class PaymentSuccessView(TemplateView):
    template_name = 'payment_youkassa/payment_success.html'



@method_decorator(csrf_exempt, name='dispatch')
class WebhookView(View):
    def post(self, request):
        try:
            notification = WebhookNotification(json.loads(request.body))
            if notification.event == 'payment.succeeded':
                youkassa_payment = notification.object
                payment = Payment.objects.get(payment_id=youkassa_payment.id)
                payment.status = 'succeeded'
                payment.save()
                buyer = payment.user
                buyer.time_left += int(float(payment.amount) * float(settings.RUB_TO_MINUTE_KOEF))
                buyer.save()
            return JsonResponse({'status': 'ok'})
        except Payment.DoesNotExist:
            return HttpResponseBadRequest("Payment not found")
        except Exception as e:
            return HttpResponseBadRequest("Error processing webhook")
