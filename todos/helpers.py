from django.urls import reverse
from django.http import HttpResponseRedirect

def not_auth_redirect():
    url = reverse("sevo-auth-login")
    return HttpResponseRedirect(url)