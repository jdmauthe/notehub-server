from django.db import models
from django.contrib.auth.models import User


# Create your models here.
def user_upload_path(instance, filename):
    return "{0}/{1}".format(instance.note.id, filename)


class Note(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    university = models.CharField(max_length=50)
    course = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class NoteFile(models.Model):
    note = models.ForeignKey(Note, on_delete=models.CASCADE)
    index = models.IntegerField()
    file = models.FileField(upload_to=user_upload_path)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ["note", "index"]
