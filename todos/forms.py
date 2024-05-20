from typing import Any, Mapping
from django import forms
from django.core.files.base import File
from django.db.models.base import Model
from django.forms.utils import ErrorList
from . import models
from django.utils.translation import gettext_lazy as _
from tinymce.widgets import TinyMCE


class TodoForm(forms.ModelForm):
    class Meta:
        model = models.Todo
        fields = "__all__"
        exclude = ["user"]
        labels = {
            "title": _("title_lbl"),
            "content": _("content_lbl"),
            "tags": _("tags_slt"), 
            "done": _("done_lbl"),
            "created_at": _("created_at_lbl"),
            "updated_at": _("updated_at_lbl")
        }
        widgets = {
            #"user": forms.HiddenInput(),
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "content": TinyMCE(attrs={"cols": 80, "rows": 30, "class": "form-control"}),
            "tags": forms.SelectMultiple(attrs={"class": "form-select multiple"}),
            "done": forms.CheckboxInput(attrs={"class": "form-check-input"})
        }

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        logged_user = request.user
        self.fields["tags"].queryset = models.Tag.objects.filter(user=logged_user)


class TagForm(forms.ModelForm):
    class Meta:
        model = models.Tag
        fields = "__all__"
        exclude = ["user"]
        labels = {
            "name": _("tag_name_lbl")
        }
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"})
        }
