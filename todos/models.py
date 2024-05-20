from django.db import models
from tinymce import models as tinymce_models
from django.contrib import admin

from django.contrib.auth import get_user_model

# Create your models here.

#from django.contrib.auth.models import User


User = get_user_model()


class Tag(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ["name"]


class Todo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = tinymce_models.HTMLField()
    tags = models.ManyToManyField(Tag, blank=True)
    done = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    class Meta:
        ordering = ["-updated_at"]


    @admin.display(description="Tags")
    def get_tags_by_user_str(self, user):
        tags = self.tags.all().filter(user=user)
        tags_list = [tag.name for tag in tags]
        return ", ".join(tags_list)

    def __str__(self):
        return f"{self.title}"
