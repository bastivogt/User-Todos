from django.shortcuts import render

from . import helpers

# Create your views here.


def index(request):
    if not request.user.is_authenticated:
        return helpers.not_auth_redirect()


    return render(request, "todos/index.html", {
        "title": "Index Todos"
    })
