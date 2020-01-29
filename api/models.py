from django.db import models
from django.contrib.auth.models import User
from uuid import uuid4


# Create your models here.
def user_upload_path(instance):
    filename = str(uuid4())
    return "{0}/{1}".format(instance.user.id, filename)


class Note(models.Model):
    author_id = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    university = models.CharField(max_length=50)
    course = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


