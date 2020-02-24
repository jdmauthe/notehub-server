from django.contrib import admin
from .models import (
    Note,
    NoteFile,
    Rating,
    Comment,
    Group,
    NoteReport,
    CommentReport,
)
# Register your models here.

admin.site.register(Note)
admin.site.register(NoteFile)
admin.site.register(Rating)
admin.site.register(Comment)
admin.site.register(Group)
admin.site.register(NoteReport)
admin.site.register(CommentReport)
