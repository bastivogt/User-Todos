from django.urls import path

#from . import views
from .views import todo_views

urlpatterns = [
    path("", todo_views.index, name="todos-index"),
    path("new/", todo_views.new, name="todos-new"),
    path("update/<int:id>", todo_views.update, name="todos-update"),
    path("done/<int:id>", todo_views.done, name="todos-done"),
    path("detail/<int:id>", todo_views.detail, name="todos-detail"),
    path("delete/<int:id>", todo_views.delete, name="todos-delete")
]