from django.shortcuts import render
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password, check_password
from django.db import IntegrityError


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
    messages.add_message(request, messages.SUCCESS, _("You are logged out!"))
    return HttpResponseRedirect(url)



# login
def login(request):
    url = reverse("sevo-auth-user-detail")
    if request.method == "POST":
        form = forms.SevoLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)

            if user is not None:
                auth_login(request, user)
                messages.add_message(request, messages.SUCCESS, _("You are logged in!"))
                return HttpResponseRedirect(url)
            else:
                messages.add_message(request, messages.ERROR, _("Login failed!"))   
                return HttpResponseRedirect(url)
    else:
        form = forms.SevoLoginForm()
    return render(request, "sevo_auth/login.html", {
        "title": _("Login"),
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
            password_confirm = form.cleaned_data["password_confirm"]



            if password != password_confirm:
                messages.add_message(request, messages.ERROR, _("Failed password confirm!"))
            else:
                try:
                    user = User(username=username, email=email)
                    user.set_password(password)
                    user.save()
                    messages.add_message(request, messages.SUCCESS, _("You are signed up!"))
                    url = reverse("sevo-auth-user-detail")
                    return HttpResponseRedirect(url) 
                except IntegrityError as e:
                    messages.add_message(request, messages.ERROR, _("Failed, username allready exists!"))
                
    else:
        form = forms.SevoSignUpForm()
    
    return render(request, "sevo_auth/sign_up.html", {
        "title": _("Sign up"),
        "form": form
    })


@login_required(login_url="sevo-auth-login")
def user_detail(request):
    current_user = request.user
    greeting_word = _("Hello")
    greeting = f"{greeting_word}, {current_user.username}!"
    return render(request, "sevo_auth/user_detail.html", {
        "greeting": greeting,
        "user": current_user
    })


@login_required(login_url="sevo-auth-login")
def change_password(request):
    current_user = request.user
    if request.method == "POST":
        form = forms.SevoChangePasswordForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data["password"]
            password_confirm = form.cleaned_data["password_confirm"]
            if(password != password_confirm):
                messages.add_message(request, messages.ERROR, _("Change password failed!"))
                # url = reverse("sevo-auth-change-password")
                # return HttpResponseRedirect(url)
            else:
                current_user.set_password(password)
                current_user.save()
                messages.add_message(request, messages.SUCCESS, _("Change password successful!"))
                url = reverse("sevo-auth-logout")
                return HttpResponseRedirect(url)

                # url = reverse("sevo-auth-user-detail")
                # return HttpResponseRedirect(url)
    else:
        form = forms.SevoChangePasswordForm()

    return render(request, "sevo_auth/change_password.html", {
        "title": _("Change password"),
        "form": form
    })


@login_required(login_url="sevo-auth-login")
def change_user_data(request):
    current_user = request.user
    inital_data = {
        "username": current_user.username,
        "email": current_user.email,
    }
    if request.method == "POST":
        form = forms.SevoChangeUserDataForm(request.POST, initial=inital_data)
        
        if form.is_valid():
            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]

            current_user.username = username
            current_user.email = email
            if current_user.check_password(password):
                try:
                    current_user.save()
                    messages.add_message(request, messages.SUCCESS, _("Userdata successful changed!"))

                    url = reverse("sevo-auth-user-detail")
                    return HttpResponseRedirect(url)
                except IntegrityError as e:
                    messages.add_message(request, messages.ERROR, _("Failed, username allready exists!"))
                    url = reverse("sevo-auth-change-user-data")
                    return HttpResponseRedirect(url)
            
            else:
                messages.add_message(request, messages.ERROR, _("Failed, wrong password!"))


    else:
        form = forms.SevoChangeUserDataForm(initial=inital_data)
    return render(request, "sevo_auth/change_user_data.html", {
        "title": _("Change userdata"),
        "form": form
    })


    