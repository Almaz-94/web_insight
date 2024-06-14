from django.urls import path

from users.apps import UsersConfig
from users.views import LoginView, RegisterView, LogoutView, UserProfileView, verify, PasswordRecoveryView

app_name = UsersConfig.name
urlpatterns = [
    path('', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('<int:pk>', UserProfileView.as_view(), name='profile'),
    path('verify/', verify, name='verification'),
    path('recovery/', PasswordRecoveryView.as_view(), name='recovery'),

]