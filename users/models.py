from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
def user_avatar_path(instance, filename):
    return "{0}/{1}".format(instance.username, filename)

class User(AbstractUser):
    avatar = models.ImageField(upload_to=user_avatar_path, blank=True)
