from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.forms import Form

from users.models import User


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class UserRegisterForm(StyleFormMixin, UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class UserLoginForm(StyleFormMixin, AuthenticationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password',)


class PasswordRecoveryForm(StyleFormMixin, Form):
    email = forms.EmailField(label="Почта")


class VerificationForm(StyleFormMixin, Form):
    number = forms.IntegerField(label='Номер')
