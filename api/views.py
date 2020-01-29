from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import generics, mixins, permissions, status
from .models import Note, NoteFile
from .permissions import IsAuthorOrReadOnly, IsNoteAuthorOrReadOnly
from .serializers import UserSerializer, NoteSerializer, NoteFileSerializer

# Create your views here.
class UserView(mixins.CreateModelMixin,
               mixins.ListModelMixin,
               generics.GenericAPIView):
    permission_classes = (permissions.AllowAny,)
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class NoteView(mixins.CreateModelMixin,
               mixins.ListModelMixin,
               generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = Note.objects.all()
    serializer_class = NoteSerializer


    def get_queryset(self):
        queryset = Note.objects.all()
        username = self.request.query_params.get('username', None)
        title = self.request.query_params.get('title', None)
        university = self.request.query_params.get('university', None)
        course = self.request.query_params.get('course', None)
        order_by = self.request.query_params.get('order_by', None)
        if username is not None:
            queryset = queryset.filter(author__username=username)
        if title is not None:
            queryset = queryset.filter(title__contains=title)
        if university is not None:
            queryset = queryset.filter(university=university)
        if course is not None:
            queryset = queryset.filter(course=course)
        if order_by is not None:
            queryset = queryset.order_by(order_by)
        return queryset

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class NoteDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthorOrReadOnly,)
    queryset = Note.objects.all()
    serializer_class = NoteSerializer


class NoteFileView(mixins.CreateModelMixin,
                   mixins.ListModelMixin,
                   generics.GenericAPIView):
    http_method_names = ['get', 'post', 'patch', 'delete']
    permission_classes = (IsNoteAuthorOrReadOnly,)
    serializer_class = NoteFileSerializer


    def perform_create(self, serializer):
        serializer.save(note=Note.objects.get(pk=self.kwargs['note_id']))


    def get_queryset(self):
            """
            This view should return a list of all the purchases for
            the user as determined by the username portion of the URL.
            """
            note_id = self.kwargs['note_id']
            return NoteFile.objects.filter(note__pk=note_id)


    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        responce = self.create(request, *args, **kwargs)
        if status.is_success(responce.status_code):
            note_id = self.kwargs['note_id']
            note = Note.objects.get(pk=note_id)
            note.save()
        return responce


class NoteFileDetailView(generics.RetrieveUpdateDestroyAPIView):
    http_method_names = ['get', 'post', 'patch', 'delete']
    permission_classes = (IsNoteAuthorOrReadOnly,)
    serializer_class = NoteFileSerializer
    lookup_field = 'index'


    def get_queryset(self):
            """
            This view should return a list of all the purchases for
            the user as determined by the username portion of the URL.
            """
            note_id = self.kwargs['note_id']
            return NoteFile.objects.filter(note__pk=note_id)
