from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.http import HttpResponseRedirect, Http404
from django.utils.translation import gettext_lazy as _
from django.contrib import messages

from todos import helpers
from todos import forms
from todos import models


# Create your views here.

def redirect_to_todos(request):
    if not request.user.is_authenticated:
        return helpers.not_auth_redirect()
    
    url = reverse("todos-index")
    return HttpResponseRedirect(url)

# index
def index(request):
    if not request.user.is_authenticated:
        return helpers.not_auth_redirect()
    
    current_user = request.user
    url = reverse("todos-index")
    
    todos = models.Todo.objects.filter(user=current_user)


    tags = models.Tag.objects.filter(user=current_user)

    # get params
    filter_tag = request.GET.get("tag")
    filter_done = request.GET.get("done")
    print(f"tag: {filter_tag}")
    print(f"tag: {filter_done}")

    #filter
    #tag
    if filter_tag != None and filter_tag != "all":
        try:
            todos = todos.filter(tags__id=int(filter_tag))
        except:
            return HttpResponseRedirect(url)
        
    #done
    if filter_done != None and filter_done != "all":
        try:
            if filter_done == "true":
                todos = todos.filter(done=True)
            elif filter_done == "false":
                todos = todos.filter(done=False)
        except:
            return HttpResponseRedirect(url)

    

    done_todos = todos.filter(done=True)
    not_done_todos = todos.filter(done=False)


    return render(request, "todos/todo/index.html", {
        "title": _("todos_index_title"),
        "todos": todos,
        "done_todos": done_todos,
        "not_done_todos": not_done_todos,
        "tags": tags
    })



# new
def new(request):
    if not request.user.is_authenticated:
        return helpers.not_auth_redirect()
    
    current_user = request.user

    todo = models.Todo(user=current_user)
    
    
    
    if request.method == "POST":
        form = forms.TodoForm(request.POST, instance=todo)
        
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, _("todos_new_success_msg"))
            url = reverse("todos-index")
            return HttpResponseRedirect(url)
        else:
            messages.add_message(request, messages.SUCCESS, _("todos_new_success_msg"))
            url = reverse("todos-new")
            return HttpResponseRedirect(url)

            
    else:
        form = forms.TodoForm(instance=todo)

    return render(request, "todos/todo/new.html", {
        "title": _("todos_new_title"),
        "send_btn_title": _("todos_send_btn_title"),
        "form": form
    })


# update
def update(request, id):
    if not request.user.is_authenticated:
        return helpers.not_auth_redirect()
    
    current_user = request.user

    todo = get_object_or_404(models.Todo, id=id, user=current_user)

    
    
    if request.method == "POST":
        form = forms.TodoForm(request.POST, instance=todo)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, _("todos_new_success_msg"))
            url = reverse("todos-index")
            return HttpResponseRedirect(url)
        else:
            messages.add_message(request, messages.SUCCESS, _("todos_new_success_msg"))
            url = reverse("todos-new")
            return HttpResponseRedirect(url)

            
    else:
        form = forms.TodoForm(instance=todo)

    return render(request, "todos/todo/new.html", {
        "title": f"{todo.title}",
        "send_btn_title": _("todos_send_btn_title"),
        "form": form
    })


# done
def done(request, id):
    if not request.user.is_authenticated:
        return helpers.not_auth_redirect()
    current_user = request.user
    todo = get_object_or_404(models.Todo, id=id, user=current_user)
    msg_done = f'{todo.title}: {_("todos_done_msg_done")}'
    msg_not_done = f'{todo.title}: {_("todos_done_msg_not_done")}'

    todo.done = not todo.done
    todo.save()

    if todo.done:
        messages.add_message(request, messages.SUCCESS, msg_done)
    else:
        messages.add_message(request, messages.WARNING, msg_not_done) 
    url = reverse("todos-index")
    return HttpResponseRedirect(url)



# detail
def detail(request, id):
    if not request.user.is_authenticated:
        return helpers.not_auth_redirect()
    
    current_user = request.user
    
    todo = get_object_or_404(models.Todo, id=id, user=current_user)
    
    return render(request, "todos/todo/detail.html", {
        "title": _("todos_detail_title"),
        "todo": todo
    })


# delete
def delete(request, id):
    if not request.user.is_authenticated:
        return helpers.not_auth_redirect()
    
    current_user = request.user
    todo = get_object_or_404(models.Todo, id=id, user=current_user)

    if request.method == "POST":
        todo.delete()
        messages.add_message(request, messages.ERROR, f'{todo.title}, {_("todos_delete_msg")}')
        url = reverse("todos-index")
        return HttpResponseRedirect(url)


    
    return render(request, "todos/todo/delete.html", {
        "title": _("todos_delete_title"),
        "todo": todo
    })
