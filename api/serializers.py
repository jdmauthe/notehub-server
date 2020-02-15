from django.contrib.auth.models import User
from django.core.validators import (
    FileExtensionValidator,
    MinValueValidator,
    MaxValueValidator,
)
from rest_framework.validators import UniqueTogetherValidator
from .models import (
    Note,
    NoteFile,
    University,
    Rating,
    Comment,
    Group,
    Membership,
    Invitation,
)
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "first_name", "last_name", "username", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, data):
        user = User(
            email=data["email"],
            first_name=data["first_name"],
            last_name=data["last_name"],
            username=data["username"],
        )
        user.set_password(data["password"])
        user.save()
        return user


class NoteSerializer(serializers.ModelSerializer):
    author = serializers.HiddenField(default="author.id")
    author_username = serializers.ReadOnlyField(source="author.username")
    university_name = serializers.ReadOnlyField(source="university.name")
    group = serializers.ReadOnlyField(source="group.id")

    class Meta:
        model = Note
        fields = [
            "id",
            "author",
            "author_username",
            "title",
            "university",
            "university_name",
            "course",
            "group",
            "created_at",
            "updated_at",
        ]
        extra_kwargs = {"university": {"write_only": True}}


class NoteFileSerializer(serializers.ModelSerializer):
    note = serializers.ReadOnlyField(source="note.id")

    class Meta:
        model = NoteFile
        fields = [
            "note",
            "index",
            "file",
            "created_at",
        ]
        extra_kwargs = {
            "file": {"validators": [FileExtensionValidator(["pdf", "png", "jpg"])],}
        }


class UniversitySerializer(serializers.ModelSerializer):
    class Meta:
        model = University
        fields = [
            "id",
            "name",
        ]


class RatingSerializer(serializers.ModelSerializer):
    note = serializers.HiddenField(default="note.id")
    author = serializers.HiddenField(default="author.id")
    username = serializers.ReadOnlyField(source="author.username")

    class Meta:
        model = Rating
        fields = [
            "id",
            "note",
            "author",
            "username",
            "score",
        ]
        extra_kwargs = {
            "score": {"validators": [MinValueValidator(0), MaxValueValidator(5),]}
        }


class CommentSerializer(serializers.ModelSerializer):
    note = serializers.HiddenField(default="note.id")
    author = serializers.HiddenField(default="author.id")
    username = serializers.ReadOnlyField(source="author.username")

    class Meta:
        model = Comment
        fields = [
            "id",
            "note",
            "author",
            "username",
            "text",
        ]


class GroupSerializer(serializers.ModelSerializer):
    moderator = serializers.HiddenField(default="moderator.id")
    moderator_username = serializers.ReadOnlyField(source="moderator.username")

    class Meta:
        model = Group
        fields = [
            "id",
            "name",
            "moderator",
            "moderator_username",
        ]


class MembershipSerializer(serializers.ModelSerializer):
    group = serializers.ReadOnlyField(source="group.id")
    group_name = serializers.ReadOnlyField(source="group.name")
    user = serializers.ReadOnlyField(source="user.id")
    username = serializers.ReadOnlyField(source="user.username")

    class Meta:
        model = Membership
        fields = [
            "id",
            "group",
            "group_name",
            "user",
            "username",
        ]


class InvitationSerializer(serializers.ModelSerializer):
    group = serializers.ReadOnlyField(source="group.id")
    group_name = serializers.ReadOnlyField(source="group.name")
    username = serializers.ReadOnlyField(source="user.username")

    class Meta:
        model = Invitation
        fields = [
            "id",
            "group",
            "group_name",
            "user",
            "username",
        ]
