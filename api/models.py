from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()


# Create your models here.
def user_upload_path(instance, filename):
    return "{0}/{1}".format(instance.note.id, filename)


class University(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Group(models.Model):
    name = models.CharField(max_length=200)
    moderator = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Note(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    university = models.ForeignKey(University, models.SET_NULL, blank=True, null=True)
    course = models.CharField(max_length=50)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_avg_rating(self):
        ratings = Rating.objects.filter(note=self.id)
        if len(ratings) == 0:
            return 0
        total = 0
        for rating in ratings:
            total += rating.score
        return total / len(ratings)

    def __str__(self):
        return self.title


class NoteFile(models.Model):
    note = models.ForeignKey(Note, on_delete=models.CASCADE)
    index = models.IntegerField()
    file = models.FileField(upload_to=user_upload_path)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ["note", "index"]

    def __str__(self):
        return self.title


class Rating(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    note = models.ForeignKey(Note, on_delete=models.CASCADE)
    score = models.FloatField()

    class Meta:
        unique_together = ["author", "note"]

    def __str__(self):
        return self.author.username + " rating for " + self.note.title


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    note = models.ForeignKey(Note, on_delete=models.CASCADE)
    text = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.text


class Invitation(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ["group", "user"]


class Membership(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ["group", "user"]


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    note = models.ForeignKey(Note, on_delete=models.CASCADE)

    class Meta:
        unique_together = ["user", "note"]

    def __str__(self):
        return self.user.username + " favorite for " + self.note.title


class NoteReport(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    note = models.ForeignKey(Note, on_delete=models.CASCADE)

    class Meta:
        unique_together = ["user", "note"]

    def __str__(self):
        return self.user.username + " report for " + self.note.title


class CommentReport(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)

    class Meta:
        unique_together = ["user", "comment"]

    def __str__(self):
        return self.user.username + " report for " + self.comment.text
