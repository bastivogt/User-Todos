from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from . import models

# class CustomUserCreateForm(UserCreationForm):
#     class Meta:
#         model = models.CustomUser
#         fields = UserChangeForm.Meta.fields

# class CustomUserChangeForm(UserChangeForm):
#     class Meta:
#         model = models.CustomUser
#         fields = UserChangeForm.Meta.fields

