from rest_framework import permissions
from .models import Note


class IsAuthorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.author == request.user


class IsNoteAuthorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.note.author == request.user

    def has_permission(self, request, view):
        if request.method == 'POST':
            note_id = view.kwargs['note_id']
            obj = Note.objects.get(pk=note_id)
            return obj.author == request.user
        return True
