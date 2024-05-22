from django.shortcuts import render
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User


from django.urls import reverse
from django.http import HttpResponseRedirect

from django.contrib import messages

from . import forms

from django.utils.translation import gettext_lazy as _




# Create your views here.


# def login(request):
#     if request.method  == "POST":
#         username = request.POST.get("username")
#         password = request.POST.get("password")
#         user = authenticate(request, username=username, password=password)
#         url = reverse("sevo-auth-login")
        
#         if user is not None:
#             auth_login(request, user)
#             messages.add_message(request, messages.SUCCESS, _("login_success_msg"))
#             return HttpResponseRedirect(url)
#         else:
#             messages.add_message(request, messages.ERROR, _("login_failed_msg"))

    
#     return render(request, "sevo_auth/login.html", {
#         "title": _("login_title")
#     })


# logout
def logout(request):
    url = reverse("sevo-auth-login")
    auth_logout(request)
    messages.add_message(request, messages.ERROR, _("sevo_auth_logout_msg"))
    return HttpResponseRedirect(url)



# login
def login(request):
    url = reverse("sevo-auth-login")
    if request.method == "POST":
        form = forms.SevoLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)

            if user is not None:
                auth_login(request, user)
                messages.add_message(request, messages.SUCCESS, _("sevo_auth_login_success_msg"))
                return HttpResponseRedirect(url)
            else:
                messages.add_message(request, messages.ERROR, _("sevo_auth_login_failed_msg"))   
                return HttpResponseRedirect(url)
    else:
        form = forms.SevoLoginForm()
    return render(request, "sevo_auth/login.html", {
        "title": _("sevo_auth_login_title"),
        "form": form
    })


# sign_up
def sign_up(request):
    if request.method == "POST":
        form = forms.SevoSignUpForm(request.POST)
        if form.is_valid():
            print("form valid")
            email = form.cleaned_data["email"]
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            try:
                user = User.objects.get(username=username)
                messages.add_message(request, messages.ERROR, _("sevo_auth_sign_up_error_user_exists_msg"))
                # url("sevo-auth-sign_up")
                # return HttpResponseRedirect(url)
            except:
                user = User(username=username, email=email)
                user.set_password(password)
                user.save()
                messages.add_message(request, messages.SUCCESS, _("sevo_auth_sign_up_success_msg"))
                url = reverse("sevo-auth-login")
                return HttpResponseRedirect(url)
    else:
        form = forms.SevoSignUpForm()
    
    return render(request, "sevo_auth/sign_up.html", {
        "title": _("sevo_auth_sign_up_title"),
        "form": form
    })


    