from django.shortcuts import render
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout

from django.urls import reverse
from django.http import HttpResponseRedirect

from django.contrib import messages

from django.utils.translation import gettext_lazy as _




# Create your views here.


def login(request):
    if request.method  == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        url = reverse("sevo-auth-login")
        
        if user is not None:
            auth_login(request, user)
            messages.add_message(request, messages.SUCCESS, _("login_success_msg"))
            return HttpResponseRedirect(url)
        else:
            messages.add_message(request, messages.ERROR, _("login_failed_msg"))

    
    return render(request, "sevo_auth/login.html", {
        "title": _("login_title")
    })


def logout(request):
    url = reverse("sevo-auth-login")
    auth_logout(request)
    messages.add_message(request, messages.ERROR, _("logout_msg"))
    return HttpResponseRedirect(url)



    