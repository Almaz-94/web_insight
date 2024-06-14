from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.forms import Form, ModelForm

from users.models import User


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class UserRegisterForm(StyleFormMixin, UserCreationForm):

    class Meta:
        model = User
        fields = ('email','password1', 'password2')


class UserLoginForm(StyleFormMixin, AuthenticationForm):

    class Meta:
        model = User
        fields = ('email','password',)


class PasswordRecoveryForm(Form):
    email = forms.EmailField(label="Почта")

