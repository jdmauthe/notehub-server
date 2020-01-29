from django.contrib.auth.models import User
from .models import Note, NoteFile
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "first_name", "last_name", "username", "password"]
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
    author = serializers.ReadOnlyField(source="author.id")

    class Meta:
        model = Note
        fields = [
            "id",
            "author",
            "title",
            "university",
            "course",
            "created_at",
            "updated_at",
        ]

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
