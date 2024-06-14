import random
import string
from random import randint

from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView as BaseLoginView, LogoutView as BaseLogoutView
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, DetailView, FormView

from users.forms import UserLoginForm, UserRegisterForm, PasswordRecoveryForm
from users.models import User


class LoginView(BaseLoginView):
    template_name = 'users/login.html'
    form_class = UserLoginForm
    success_url = reverse_lazy('main:request_summary')


class PasswordRecoveryView(FormView):
    form_class = PasswordRecoveryForm
    template_name = 'users/password_recovery.html'
    success_url = reverse_lazy('user:login')

    def form_valid(self, form):
        try:

            user = User.objects.get(email=form.cleaned_data['email'])
        except ObjectDoesNotExist:
            form.add_error('email', 'С указанной почтой не связан ни один аккаунт')
            return self.form_invalid(form)
        new_password = ''.join([random.choice(string.ascii_letters + string.digits) for _ in range(10)])
        send_mail(
            subject='Your new password',
            message=new_password,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email],
            fail_silently=False
        )

        user.set_password(new_password)
        user.save()
        return super().form_valid(form)

class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('user:verification')

    def form_valid(self, form):
        new_user = form.save()
        new_user.is_active = False
        ver_num = randint(1000, 1000000)
        new_user.verification_code = ver_num
        new_user.save()
        send_mail(
            subject='Account activation',
            message=f'Your activation code : {ver_num}',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[new_user.email],
            fail_silently=False
        )
        return super().form_valid(form)


def verify(request):
    if request.method == 'POST':
        number = request.POST.get('number')
    try:
        user = User.objects.get(verification_code=number)
        user.is_active = True
        user.save()
        return redirect(reverse('user:login'))
    except ObjectDoesNotExist:
        return render(request, 'users/verification.html')


class UserProfileView(LoginRequiredMixin, DetailView):
    context_object_name = 'user'
    model = User


class LogoutView(BaseLogoutView):
    next_page = reverse_lazy('user:login')
