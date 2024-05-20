
from django.contrib import admin



# Register your models here.
from . import models

from django.contrib.auth.models import User


class TagsFilter(admin.SimpleListFilter):
    title = "Tag"
    parameter_name = "tag"

    def lookups(self, request, model_admin):
        user = request.user
        qs = models.Tag.objects.all()
        if not user.is_superuser:
            qs = qs.filter(user=user)

        return ((obj.id, obj.name) for obj in qs)

    def queryset(self, request, queryset):
        if self.value():
            queryset = queryset.filter(tags__id=self.value())
        return queryset



class TodoAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "created_at",
        "updated_at",
        "done"
        ]
    
    list_filter = [
        "user",
        TagsFilter,
        "done"
    ]
    
    def get_queryset(self, request):
        q = super().get_queryset(request)
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
        

    def get_field_queryset(self, db, db_field, request):
        """
        If the ModelAdmin specifies ordering, the queryset should respect that
        ordering.  Otherwise don't specify the queryset, let the field decide
        (returns None in that case).
        """
        user = request.user
        if db_field.name == 'tags':

            return db_field.remote_field.model._default_manager.filter(
                              user=user,
            )

        super().get_field_queryset(db, db_field, request)
        

    
    # def get_object(self, request, object_id, from_field):
    #     o = super().get_object(request, object_id, from_field)
    #     if request.user.is_superuser:
    #         return o
    #     else:
    #         if o.user == request.user:
    #             return o
    #         return None




# TagAdmin
class TagAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "user"
    ]

    list_filter = [
        "user"
    ]

    def get_list_filter(self, request):
        lf = super().get_list_filter(request)
        if request.user.is_superuser:
            return lf
        else:
            new_lf = [item for item in lf if item != "user"]
            return new_lf


    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if request.user.is_superuser:
            return super().formfield_for_foreignkey(db_field, request, **kwargs)
        
        if db_field.name == "user":
            kwargs["queryset"] = User.objects.filter(id=request.user.id)
            return super().formfield_for_foreignkey(db_field, request, **kwargs)
        


    def get_queryset(self, request):
        q = super().get_queryset(request)
        if request.user.is_superuser:
            return q
        else:
            logged_user = request.user
            return q.filter(user=logged_user)
        


admin.site.register(models.Todo, TodoAdmin)
admin.site.register(models.Tag, TagAdmin)
