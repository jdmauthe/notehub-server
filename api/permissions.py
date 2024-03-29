from rest_framework import permissions
from django.core.exceptions import ObjectDoesNotExist
from .models import (
    Note,
    Rating,
    Membership,
    Group,
    Invitation,
    Favorite,
    NoteReport,
    CommentReport,
)


class IsAuthor(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        user = None
        try:
            user = obj.user
        except AttributeError:
            user = obj.author
        return user == request.user


class IsAuthorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        user = None
        try:
            user = obj.user
        except AttributeError:
            user = obj.author
        return user == request.user


class IsModeratorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.moderator == request.user


class IsAuthorOrModeratorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        user = None
        try:
            user = obj.user
        except AttributeError:
            user = obj.author
        if user == request.user:
            return True
        if obj.group is not None:
            return obj.group.moderator == request.user
        return False


class CanAccessNote(permissions.BasePermission):
    def has_permission(self, request, view):
        note_id = view.kwargs.get("note_id")
        if note_id is None:
            note_id = view.kwargs.get("pk")
        note = None
        try:
            note = Note.objects.get(pk=note_id)
        except ObjectDoesNotExist:
            return False
        if note.author == request.user:
            return True
        if note.group is None:
            return True
        if request.user.is_anonymous:
            return False
        return (
            Membership.objects.all()
            .filter(user=request.user)
            .filter(group=note.group)
            .exists()
        )


class CanAccessGroup(permissions.BasePermission):
    def has_permission(self, request, view):
        group_id = view.kwargs.get("group_id")
        if group_id is None:
            group_id = view.kwargs.get("pk")
        group = Group.objects.get(pk=group_id)
        return (
            Membership.objects.all()
            .filter(user=request.user)
            .filter(group=group.id)
            .exists()
        )


class HasInvitation(permissions.BasePermission):
    def has_permission(self, request, view):
        group_id = view.kwargs.get("group_id")
        if group_id is None:
            group_id = view.kwargs.get("pk")
        group = Group.objects.get(pk=group_id)
        if request.method == "POST":
            return (
                Invitation.objects.all()
                .filter(user=request.user)
                .filter(group=group.id)
                .exists()
            )
        return (
            Membership.objects.all()
            .filter(user=request.user)
            .filter(group=group.id)
            .exists()
        )


class IsModerator(permissions.BasePermission):
    def has_permission(self, request, view):
        group_id = view.kwargs.get("group_id")
        if group_id is None:
            group_id = view.kwargs.get("pk")
        group = Group.objects.get(pk=group_id)
        return request.user == group.moderator


class IsModeratorOrInvitee(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        group_id = view.kwargs.get("group_id")
        if group_id is None:
            group_id = view.kwargs.get("pk")
        group = Group.objects.get(pk=group_id)
        return request.user == group.moderator or request.user == obj.user


class IsNoteAuthorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.note.author == request.user

    def has_permission(self, request, view):
        if request.method == "POST":
            note_id = view.kwargs["note_id"]
            obj = Note.objects.get(pk=note_id)
            return obj.author == request.user
        return True


class AlreadyPostedRating(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == "POST":
            note_id = view.kwargs["note_id"]
            obj = Rating.objects.all()
            return (
                not obj.filter(note__pk=note_id)
                .filter(author__pk=request.user.id)
                .exists()
            )
        return True


class AlreadyPostedFavorite(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == "POST":
            note_id = view.kwargs["note_id"]
            obj = Favorite.objects.all()
            return (
                not obj.filter(note__pk=note_id)
                .filter(user__pk=request.user.id)
                .exists()
            )
        return True


class AlreadyPostedNoteReport(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == "POST":
            note_id = view.kwargs["note_id"]
            obj = NoteReport.objects.all()
            return (
                not obj.filter(note__pk=note_id)
                .filter(user__pk=request.user.id)
                .exists()
            )
        return True


class AlreadyPostedCommentReport(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == "POST":
            comment_id = view.kwargs["comment_id"]
            obj = CommentReport.objects.all()
            return (
                not obj.filter(comment__pk=comment_id)
                .filter(user__pk=request.user.id)
                .exists()
            )
        return True


class CanAccessFavorite(permissions.BasePermission):
    def has_permission(self, request, view):
        note_id = view.kwargs.get("note_id")
        if note_id is None:
            note_id = view.kwargs.get("pk")
        note = None
        try:
            note = Note.objects.get(pk=note_id)
        except ObjectDoesNotExist:
            return False
        if note.author == request.user:
            return True
        if note.group is None:
            return True
        if request.user.is_anonymous:
            return False
        is_member = (
            Membership.objects.all()
            .filter(user=request.user)
            .filter(group=note.group)
            .exists()
        )
        is_get = request.method == "GET"
        return is_member or is_get
