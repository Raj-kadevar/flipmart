from django.contrib.auth import forms, get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from user.models import User

from django.contrib.auth import authenticate
class Registration(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

#
# class Login(AuthenticationForm):
#     class Meta:
#         model = User
#         fields = ['username', 'password']
