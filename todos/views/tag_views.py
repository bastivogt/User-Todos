from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.utils.translation import gettext_lazy as _
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from todos import models
from todos import helpers
from todos import forms

@login_required(login_url="sevo-auth-login")
def tag_index(request):
    
    tags = models.Tag.objects.all()
    current_user = request.user
    tags = tags.filter(user=current_user)

    return render(request, "todos/tag/index.html", {
        "title": _("Tags"),
        "tags": tags
    })


# new
@login_required(login_url="sevo-auth-login")
def tag_new(request):
    
    current_user = request.user

    tag = models.Tag(user=current_user)
    
    
    if request.method == "POST":
        form = forms.TagForm(request.POST, instance=tag)
        
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, _("Tag created!"))
            url = reverse("todos-tag-index")
            return HttpResponseRedirect(url)
        else:
            messages.add_message(request, messages.ERROR, _("Failed, tag not created!"))


            
    else:
        form = forms.TagForm( instance=tag)

    return render(request, "todos/tag/new.html", {
        "title": _("New tag"),
        "send_btn_title": _("Create"),
        "form": form
    })


#update
@login_required(login_url="sevo-auth-login")
def tag_update(request, id):
    
    current_user = request.user

    tag = get_object_or_404(models.Tag, id=id, user=current_user)
    
    
    if request.method == "POST":
        form = forms.TagForm(request.POST, instance=tag)
        
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, _("Tag updated!"))
            url = reverse("todos-tag-index")
            return HttpResponseRedirect(url)
        else:
            messages.add_message(request, messages.ERROR, _("Failed, tag not updated!"))


            
    else:
        form = forms.TagForm( instance=tag)

    return render(request, "todos/tag/new.html", {
        "title": _("Update tag"),
        "send_btn_title": _("Update"),
        "form": form
    })


#delete
@login_required(login_url="sevo-auth-login")
def tag_delete(request, id):
    
    current_user = request.user
    url = reverse("todos-tag-index")
    
    tag = get_object_or_404(models.Tag, id=id, user=current_user)

    if request.method == "POST":
        tag.delete()
        delete_msg = _("deleted")
        messages.add_message(request, messages.ERROR, f'{tag.name}, {delete_msg}!')
        return HttpResponseRedirect(url)

    
    return render(request, "todos/tag/delete.html", {
        "title": _("Delete tag"),
        "tag": tag
    })