from django.urls import path

#from . import views
from .views import todo_views
from .views import tag_views

urlpatterns = [
    path("", todo_views.index, name="todos-index"),
    path("new/", todo_views.new, name="todos-new"),
    path("update/<int:id>", todo_views.update, name="todos-update"),
    path("done/<int:id>", todo_views.done, name="todos-done"),
    path("detail/<int:id>", todo_views.detail, name="todos-detail"),
    path("delete/<int:id>", todo_views.delete, name="todos-delete"),

    path("tags/", tag_views.tag_index, name="todos-tag-index"),
    path("tag/new", tag_views.tag_new, name="todos-tag-new"),
    path("tag/update/<int:id>", tag_views.tag_update, name="todos-tag-update"),
    path("tag/delete/<int:id>", tag_views.tag_delete, name="todos-tag-delete"),
]