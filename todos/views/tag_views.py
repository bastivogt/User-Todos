from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.utils.translation import gettext_lazy as _

from todos import models
from todos import helpers


def tag_index(request):
    if not request.user.is_authenticated:
        return helpers.not_auth_redirect()
    
    tags = models.Tag.objects.all()
    current_user = request.user
    tags = tags.filter(user=current_user)

    return render(request, "todos/tag/index.html", {
        "title": _("tag_index_title"),
        "tags": tags
    })


def tag_new(request):
    pass