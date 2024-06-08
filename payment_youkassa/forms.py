from django import forms
from django.core.validators import MinValueValidator

from payment_youkassa.models import Payment


class PaymentForm(forms.ModelForm):
    amount = forms.IntegerField(validators=[MinValueValidator(1)], label='Сумма')
    class Meta:
        model = Payment
        fields = ('amount', )

    # amount = forms.IntegerField(validators=[MinValueValidator(1)], label='Сумма', widget=forms.NumberInput(attrs={'inputmode': 'numeric'}))
    # amount = forms.DecimalField(
    #     label='Amount',
    #     widget=forms.NumberInput(attrs={'inputmode': 'numeric'}),
    # )