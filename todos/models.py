from django.db import models
from tinymce import models as tinymce_models

from django.contrib.auth import get_user_model

# Create your models here.

#from django.contrib.auth.models import User


User = get_user_model()

class Todo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = tinymce_models.HTMLField()
    done = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    class Meta:
        ordering = ["-updated_at"]


    def __str__(self):
        return f"{self.title}"
