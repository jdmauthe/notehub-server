from django.contrib.auth.models import User
from django.core.validators import (
    FileExtensionValidator,
    MinValueValidator,
    MaxValueValidator,
    DecimalValidator,
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
    Favorite,
    NoteReport,
    CommentReport,
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
    avg_rating = serializers.ReadOnlyField(source="get_avg_rating")

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
            "avg_rating",
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
    note = serializers.ReadOnlyField(source="note.id")
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
    moderator = serializers.ReadOnlyField(source="moderator.id")
    moderator_username = serializers.ReadOnlyField(source="moderator.username")
    is_moderator = serializers.SerializerMethodField(method_name="check_if_moderator")

    def check_if_moderator(self, obj):
        user = self.context['request'].user
        return user == obj.moderator

    class Meta:
        model = Group
        fields = [
            "id",
            "name",
            "moderator",
            "moderator_username",
            "is_moderator",
        ]


class MembershipSerializer(serializers.ModelSerializer):
    group = serializers.ReadOnlyField(source="group.id")
    group_name = serializers.ReadOnlyField(source="group.name")
    user = serializers.ReadOnlyField(source="user.id")
    username = serializers.ReadOnlyField(source="user.username")
    role = serializers.SerializerMethodField(method_name="get_role")
    is_user = serializers.SerializerMethodField(method_name="check_is_user")

    def check_is_user(self, obj):
        user = self.context['request'].user
        return user == obj.user

    def get_role(self, obj):
        moderator = Group.objects.get(pk=obj.group.id).moderator
        is_moderator = obj.user == moderator
        if is_moderator:
            return "Moderator"
        else:
            return "Member"

    class Meta:
        model = Membership
        fields = [
            "id",
            "group",
            "group_name",
            "user",
            "username",
            "role",
            "is_user",
            "joined_at",
        ]


class InvitationSerializer(serializers.ModelSerializer):
    group = serializers.ReadOnlyField(source="group.id")
    group_name = serializers.ReadOnlyField(source="group.name")
    username = serializers.ReadOnlyField(source="user.username")
    moderator_username = serializers.SerializerMethodField(method_name="get_moderator")

    def get_moderator(self, obj):
        return Group.objects.get(pk=obj.group.id).moderator.username

    class Meta:
        model = Invitation
        fields = [
            "id",
            "group",
            "group_name",
            "user",
            "username",
            "moderator_username",
        ]


class FavoriteSerializer(serializers.ModelSerializer):
    note = serializers.ReadOnlyField(source="note.id")
    user = serializers.ReadOnlyField(source="user.id")

    class Meta:
        model = Favorite
        fields = [
            "id",
            "note",
            "user",
        ]


class NoteReportSerializer(serializers.ModelSerializer):
    note = serializers.ReadOnlyField(source="note.id")
    user = serializers.ReadOnlyField(source="user.id")

    class Meta:
        model = NoteReport
        fields = [
            "id",
            "note",
            "user",
        ]


class CommentReportSerializer(serializers.ModelSerializer):
    comment = serializers.ReadOnlyField(source="comment.id")
    user = serializers.ReadOnlyField(source="user.id")

    class Meta:
        model = CommentReport
        fields = [
            "id",
            "comment",
            "user",
        ]
