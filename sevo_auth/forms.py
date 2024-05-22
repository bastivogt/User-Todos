from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from django.utils.translation import gettext_lazy as _

from . import models

# class CustomUserCreateForm(UserCreationForm):
#     class Meta:
#         model = models.CustomUser
#         fields = UserChangeForm.Meta.fields

# class CustomUserChangeForm(UserChangeForm):
#     class Meta:
#         model = models.CustomUser
#         fields = UserChangeForm.Meta.fields


class SevoLoginForm(forms.Form):
    username = forms.CharField(max_length=255, label=_("username_lbl"))
    password = forms.CharField(label=_("password_lbl"), widget=forms.PasswordInput)


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs["class"] = "form-control"
        self.fields["password"].widget.attrs["class"] = "form-control"



class SevoSignUpForm(forms.Form):
    email = forms.CharField(max_length=255, widget=forms.EmailInput)
    username = forms.CharField(max_length=255, label=_("username_lbl"))
    password = forms.CharField(label=_("password_lbl"), widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["email"].widget.attrs["class"] = "form-control"
        self.fields["username"].widget.attrs["class"] = "form-control"
        self.fields["password"].widget.attrs["class"] = "form-control"
