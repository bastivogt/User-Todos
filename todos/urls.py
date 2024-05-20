from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="todos-index"),
    path("new/", views.new, name="todos-new"),
    path("update/<int:id>", views.update, name="todos-update"),
    path("done/<int:id>", views.done, name="todos-done"),
    path("detail/<int:id>", views.detail, name="todos-detail"),
    path("delete/<int:id>", views.delete, name="todos-delete")
]