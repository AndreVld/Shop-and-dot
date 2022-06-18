from django.contrib.auth.forms import UserCreationForm
from django import forms

from app_users.models import AdvUser


class RegistrationUserForm(UserCreationForm):
    class Meta:
        model = AdvUser
        fields = ('username', 'email', 'password1', 'password2',)
