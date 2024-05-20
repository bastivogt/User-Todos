from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.utils.translation import gettext_lazy as _
from django.contrib import messages

from todos import models
from todos import helpers
from todos import forms


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


# new
def tag_new(request):
    if not request.user.is_authenticated:
        return helpers.not_auth_redirect()
    
    current_user = request.user

    todo = models.Tag(user=current_user)
    
    
    
    if request.method == "POST":
        form = forms.TagForm(request.POST, instance=todo)
        
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, _("todos_tag_new_success_msg"))
            url = reverse("todos-tag-index")
            return HttpResponseRedirect(url)
        else:
            messages.add_message(request, messages.SUCCESS, _("todos_tag_new_success_msg"))
            url = reverse("todos-tag-new")
            return HttpResponseRedirect(url)

            
    else:
        form = forms.TagForm( instance=todo)

    return render(request, "todos/tag/new.html", {
        "title": _("todos_tag__new_title"),
        "send_btn_title": _("todos_send_btn_title"),
        "form": form
    })