from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.http import HttpResponseRedirect, Http404
from django.utils.translation import gettext_lazy as _
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from todos import helpers
from todos import forms
from todos import models


# Create your views here.

# redirect
def redirect_to_todos(request):
    if not request.user.is_authenticated:
        return helpers.not_auth_redirect()
    
    url = reverse("todos-index")
    return HttpResponseRedirect(url)

# index
@login_required(login_url="sevo-auth-login")
def index(request):
    # if not request.user.is_authenticated:
    #     return helpers.not_auth_redirect()
    
    current_user = request.user
    url = reverse("todos-index")
    
    # get params
    filter_tag = request.GET.get("tag")
    filter_done = request.GET.get("done")
    filter_order = request.GET.get("order")
    print(f"tag: {filter_tag}")
    print(f"done: {filter_done}")
    print(f"order: {filter_order}")
    order_str = "-created_at"

    #order
    if filter_order != None:
        print("order")
        if filter_order == "created_at_asc":
            order_str = "created_at"
            print("created_at asc")
        elif filter_order == "created_at_desc":
            order_str = "-created_at"
            print("created_at desc")
        elif filter_order == "updated_at_asc":
            order_str = "updated_at"
            print("updated_at asc")
        elif filter_order == "updated_at_desc":
            order_str = "-updated_at"
            print("updated_at desc")
    
    # modelentries
    todos = models.Todo.objects.filter(user=current_user).order_by(order_str)
    tags = models.Tag.objects.filter(user=current_user)

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

    # creating done and not_done vars
    done_todos = todos.filter(done=True)
    not_done_todos = todos.filter(done=False)

    return render(request, "todos/todo/index.html", {
        "title": _("Todos"),
        "todos": todos,
        "done_todos": done_todos,
        "not_done_todos": not_done_todos,
        "tags": tags
    })



# new
@login_required(login_url="sevo-auth-login")
def new(request):
    current_user = request.user

    todo = models.Todo(user=current_user)
    
    
    
    if request.method == "POST":
        form = forms.TodoForm(request.POST, instance=todo)
        
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, _("Todo created!"))
            url = reverse("todos-index")
            return HttpResponseRedirect(url)
        else:
            messages.add_message(request, messages.ERROR, _("Failed, todo not created!"))


            
    else:
        form = forms.TodoForm(instance=todo)

    return render(request, "todos/todo/new.html", {
        "title": _("New todo"),
        "send_btn_title": _("Create"),
        "form": form
    })


# update
@login_required(login_url="sevo-auth-login")
def update(request, id):
    
    current_user = request.user

    todo = get_object_or_404(models.Todo, id=id, user=current_user)

    
    
    if request.method == "POST":
        form = forms.TodoForm(request.POST, instance=todo)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, _("Todo updated!"))
            url = reverse("todos-detail", args=[id])
            return HttpResponseRedirect(url)
        else:
            messages.add_message(request, messages.ERROR, _("Failed, todo not updated!"))


            
    else:
        form = forms.TodoForm(instance=todo)

    return render(request, "todos/todo/new.html", {
        "title": f"{todo.title}",
        "send_btn_title": _("Update"),
        "form": form
    })


# done
@login_required(login_url="sevo-auth-login")
def done(request, id):
    current_user = request.user
    todo = get_object_or_404(models.Todo, id=id, user=current_user)
    msg_done = _("done")
    msg_not_done = _("not done")
    msg_done_full = f'{todo.title}: {msg_done}'
    msg_not_done_full = f'{todo.title}: {msg_not_done}'

    todo.done = not todo.done
    todo.save()

    if todo.done:
        messages.add_message(request, messages.SUCCESS, msg_done_full)
    else:
        messages.add_message(request, messages.WARNING, msg_not_done_full) 
    url = reverse("todos-index")
    return HttpResponseRedirect(url)



# detail
@login_required(login_url="sevo-auth-login")
def detail(request, id):
    current_user = request.user
    
    todo = get_object_or_404(models.Todo, id=id, user=current_user)
    
    return render(request, "todos/todo/detail.html", {
        "title": _("Todo detail"),
        "todo": todo
    })


# delete
@login_required(login_url="sevo-auth-login")
def delete(request, id):
    
    current_user = request.user
    todo = get_object_or_404(models.Todo, id=id, user=current_user)

    if request.method == "POST":
        todo.delete()
        delete_msg = _("deleted")
        messages.add_message(request, messages.ERROR, f'{todo.title}, {delete_msg}')
        url = reverse("todos-index")
        return HttpResponseRedirect(url)


    
    return render(request, "todos/todo/delete.html", {
        "title": _("Delete todo"),
        "todo": todo
    })
