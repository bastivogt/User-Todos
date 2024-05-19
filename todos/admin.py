
from collections.abc import Sequence
from typing import Any
from django.contrib import admin
from django.db.models.fields.related import RelatedField
from django.db.models.query import QuerySet
from django.http import HttpRequest

# Register your models here.
from . import models

from django.contrib.auth.models import User


class TodoAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "user",
        "created_at",
        "updated_at",
        "done"
        ]
    
    list_filter = [
        "user",
        "done"
    ]
    
    def get_queryset(self, request):
        q = super(TodoAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return q
        else:
            logged_user = request.user
            return q.filter(user=logged_user)
        


        
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if request.user.is_superuser:
            return super().formfield_for_foreignkey(db_field, request, **kwargs)
        
        if db_field.name == "user":
            kwargs["queryset"] = User.objects.filter(id=request.user.id)
            return super().formfield_for_foreignkey(db_field, request, **kwargs)



    def get_list_filter(self, request):
        lf = super().get_list_filter(request)
        if request.user.is_superuser:
            return lf
        else:
            new_lf = [item for item in lf if item != "user"]
            return new_lf
        
    # def get_object(self, request, object_id, from_field):
    #     o = super().get_object(request, object_id, from_field)
    #     if request.user.is_superuser:
    #         return o
    #     else:
    #         if o.user == request.user:
    #             return o
    #         return None


admin.site.register(models.Todo, TodoAdmin)
