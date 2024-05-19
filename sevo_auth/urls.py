from django.urls import path
from  . import views


urlpatterns = [
    path("login/", views.login, name="sevo-auth-login"),
    path("logout", views.logout, name="sevo-auth-logout"),
]


