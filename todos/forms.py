from django import forms
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
            "done": _("done_lbl"),
            "created_at": _("created_at_lbl"),
            "updated_at": _("updated_at_lbl")
        }
        widgets = {
            "user": forms.HiddenInput(),
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "content": TinyMCE(attrs={"cols": 80, "rows": 30, "class": "form-control"}),
            "done": forms.CheckboxInput(attrs={"class": "form-check-input"})
        }