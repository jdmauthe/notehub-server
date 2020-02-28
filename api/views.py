from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import generics, mixins, permissions, status
from rest_framework.response import Response
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
from .permissions import (
    IsAuthor,
    IsAuthorOrReadOnly,
    IsAuthorOrModeratorOrReadOnly,
    IsModeratorOrReadOnly,
    IsNoteAuthorOrReadOnly,
    AlreadyPostedRating,
    AlreadyPostedFavorite,
    AlreadyPostedNoteReport,
    AlreadyPostedCommentReport,
    CanAccessNote,
    CanAccessGroup,
    CanAccessFavorite,
    HasInvitation,
    IsModerator,
)
from .serializers import (
    UserSerializer,
    NoteSerializer,
    NoteFileSerializer,
    UniversitySerializer,
    RatingSerializer,
    CommentSerializer,
    MembershipSerializer,
    GroupSerializer,
    InvitationSerializer,
    FavoriteSerializer,
    NoteReportSerializer,
    CommentReportSerializer,
)

# Create your views here.
class UserView(mixins.CreateModelMixin, mixins.ListModelMixin, generics.GenericAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserSerializer

    def get_queryset(self):
        queryset = User.objects.all()
        username = self.request.query_params.get("username", None)
        if username is not None:
            queryset = queryset.filter(username=username)
        return queryset

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class SelfView(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        user = User.objects.get(id=request.user.id)
        serializer = UserSerializer(user, many=False)
        return Response(serializer.data)


class SelfNoteView(mixins.ListModelMixin, generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = NoteSerializer

    def get_queryset(self):
        user = self.request.user
        return Note.objects.filter(author__id=user.id)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class SelfGroupView(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

    def get(self, request, *args, **kwargs):
        memberships = Membership.objects.filter(user__id=request.user.id)
        id_list = []
        for membership in memberships:
            id_list.append(membership.group.id)
        groups = Group.objects.filter(id__in=id_list)
        serializer = GroupSerializer(groups, many=True, context={'request': request})
        return Response(serializer.data)


class SelfFavoritesView(mixins.ListModelMixin, generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = NoteSerializer

    def get_queryset(self):
        user = self.request.user
        favorites = Favorite.objects.filter(user__id=user.id)
        id_list = []
        for favorite in favorites:
            id_list.append(favorite.note.id)
        return Note.objects.filter(id__in=id_list)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class SelfInvitationView(mixins.ListModelMixin, generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = InvitationSerializer

    def get_queryset(self):
        user = self.request.user
        return Invitation.objects.filter(user__id=user.id)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class NoteView(mixins.CreateModelMixin, mixins.ListModelMixin, generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    serializer_class = NoteSerializer

    def get_queryset(self):
        queryset = Note.objects.all().filter(group__isnull=True)
        username = self.request.query_params.get("username", None)
        title = self.request.query_params.get("title", None)
        university = self.request.query_params.get("university", None)
        course = self.request.query_params.get("course", None)
        order_by = self.request.query_params.get("order_by", None)
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
        serializer.save(author=self.request.user, group=None)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class NoteDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthorOrModeratorOrReadOnly, CanAccessNote)
    queryset = Note.objects.all()
    serializer_class = NoteSerializer


class NoteFileView(
    mixins.CreateModelMixin, mixins.ListModelMixin, generics.GenericAPIView
):
    http_method_names = ["get", "post", "patch", "delete"]
    permission_classes = (IsNoteAuthorOrReadOnly, CanAccessNote)
    serializer_class = NoteFileSerializer

    def perform_create(self, serializer):
        serializer.save(note=Note.objects.get(pk=self.kwargs["note_id"]))

    def get_queryset(self):
        note_id = self.kwargs["note_id"]
        return NoteFile.objects.filter(note__pk=note_id)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        responce = self.create(request, *args, **kwargs)
        if status.is_success(responce.status_code):
            note_id = self.kwargs["note_id"]
            note = Note.objects.get(pk=note_id)
            note.save()
        return responce


class NoteFileDetailView(generics.RetrieveUpdateDestroyAPIView):
    http_method_names = ["get", "post", "patch", "delete", "options"]
    permission_classes = (IsNoteAuthorOrReadOnly, CanAccessNote)
    serializer_class = NoteFileSerializer
    lookup_field = "index"

    def get_queryset(self):
        note_id = self.kwargs["note_id"]
        return NoteFile.objects.filter(note__pk=note_id)


class UniversityView(mixins.ListModelMixin, generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    serializer_class = UniversitySerializer

    def get_queryset(self):
        queryset = University.objects.all()
        starts_with = self.request.query_params.get("starts_with", None)
        contains = self.request.query_params.get("contains", None)
        order_by = self.request.query_params.get("order_by", None)
        if starts_with is not None:
            queryset = queryset.filter(name__startswith=starts_with)
        if contains is not None:
            queryset = queryset.filter(name__contains=contains)
        if order_by is not None:
            queryset = queryset.order_by(order_by)
        return queryset

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class UniversityDetailView(generics.RetrieveAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = University.objects.all()
    serializer_class = UniversitySerializer
    lookup_field = "name"


class RatingView(
    mixins.CreateModelMixin, mixins.ListModelMixin, generics.GenericAPIView
):
    permission_classes = (
        permissions.IsAuthenticated,
        AlreadyPostedRating,
        CanAccessNote,
    )
    serializer_class = RatingSerializer

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user, note=Note.objects.get(pk=self.kwargs["note_id"])
        )

    def get_queryset(self):
        note_id = self.kwargs["note_id"]
        return Rating.objects.filter(author=self.request.user.id).filter(note=note_id)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class RatingDetailView(generics.RetrieveUpdateDestroyAPIView):
    http_method_names = ["get", "post", "patch", "delete", "options"]
    permission_classes = (
        permissions.IsAuthenticated,
        IsAuthorOrReadOnly,
        CanAccessNote,
    )
    serializer_class = RatingSerializer

    def get_queryset(self):
        note_id = self.kwargs["note_id"]
        return Rating.objects.filter(note__pk=note_id)


class CommentView(
    mixins.CreateModelMixin, mixins.ListModelMixin, generics.GenericAPIView
):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, CanAccessNote)
    serializer_class = CommentSerializer

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user, note=Note.objects.get(pk=self.kwargs["note_id"])
        )

    def get_queryset(self):
        note_id = self.kwargs["note_id"]
        return Comment.objects.filter(note__pk=note_id)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    http_method_names = ["get", "post", "patch", "delete", "options"]
    permission_classes = (IsAuthorOrReadOnly, CanAccessNote)
    serializer_class = CommentSerializer

    def get_queryset(self):
        note_id = self.kwargs["note_id"]
        return Comment.objects.filter(note__pk=note_id)


class GroupView(mixins.CreateModelMixin, generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = GroupSerializer

    def perform_create(self, serializer):
        serializer.save(moderator=self.request.user)

    def post(self, request, *args, **kwargs):
        response = self.create(request, *args, **kwargs)
        if status.is_success(response.status_code):
            group = Group.objects.get(pk=response.data["id"])
            user = request.user
            Membership.objects.create(group=group, user=user)
        return response


class GroupDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (
        permissions.IsAuthenticated,
        IsModeratorOrReadOnly,
        CanAccessGroup,
    )
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class GroupNoteView(
    mixins.CreateModelMixin, mixins.ListModelMixin, generics.GenericAPIView
):
    permission_classes = (permissions.IsAuthenticated, CanAccessGroup)
    serializer_class = NoteSerializer

    def get_queryset(self):
        queryset = Note.objects.all().filter(group=self.kwargs["group_id"])
        username = self.request.query_params.get("username", None)
        title = self.request.query_params.get("title", None)
        university = self.request.query_params.get("university", None)
        course = self.request.query_params.get("course", None)
        order_by = self.request.query_params.get("order_by", None)
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
        serializer.save(
            author=self.request.user,
            group=Group.objects.get(pk=self.kwargs["group_id"]),
        )

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class GroupMembershipView(
    mixins.CreateModelMixin, mixins.ListModelMixin, generics.GenericAPIView
):
    permission_classes = (
        permissions.IsAuthenticated,
        HasInvitation,
    )
    serializer_class = MembershipSerializer

    def perform_create(self, serializer):
        serializer.save(
            user=self.request.user, group=Group.objects.get(pk=self.kwargs["group_id"])
        )

    def get_queryset(self):
        group_id = self.kwargs["group_id"]
        return Membership.objects.filter(group=group_id)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        response = self.create(request, *args, **kwargs)
        if status.is_success(response.status_code):
            group = Group.objects.get(pk=response.data["group"])
            Invitation.objects.all().filter(user=request.user).filter(
                group=group.id
            ).delete()
        return response


class GroupMembershipDetailView(generics.RetrieveDestroyAPIView):
    permission_classes = (
        permissions.IsAuthenticated,
        IsAuthorOrModeratorOrReadOnly,
    )
    serializer_class = MembershipSerializer

    def get_queryset(self):
        group_id = self.kwargs["group_id"]
        return Membership.objects.filter(group__pk=group_id)


class GroupInvitationView(
    mixins.CreateModelMixin, mixins.ListModelMixin, generics.GenericAPIView
):
    permission_classes = (
        permissions.IsAuthenticated,
        IsModerator,
    )
    serializer_class = InvitationSerializer

    def perform_create(self, serializer):
        serializer.save(group=Group.objects.get(pk=self.kwargs["group_id"]))

    def get_queryset(self):
        group_id = self.kwargs["group_id"]
        return Invitation.objects.filter(group=group_id)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class GroupInvitationDetailView(generics.RetrieveDestroyAPIView):
    permission_classes = (
        permissions.IsAuthenticated,
        IsModerator,
    )
    serializer_class = InvitationSerializer

    def get_queryset(self):
        group_id = self.kwargs["group_id"]
        return Invitation.objects.filter(group__pk=group_id)


class FavoriteView(
    mixins.CreateModelMixin, mixins.ListModelMixin, generics.GenericAPIView
):
    permission_classes = (
        permissions.IsAuthenticated,
        IsAuthorOrReadOnly,
        AlreadyPostedFavorite,
        CanAccessFavorite,
    )
    serializer_class = FavoriteSerializer

    def perform_create(self, serializer):
        serializer.save(
            user=self.request.user, note=Note.objects.get(pk=self.kwargs["note_id"])
        )

    def get_queryset(self):
        note_id = self.kwargs["note_id"]
        return Favorite.objects.filter(user=self.request.user.id).filter(note=note_id)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class FavoriteDetailView(generics.RetrieveDestroyAPIView):
    permission_classes = (
        permissions.IsAuthenticated,
        IsAuthor,
    )
    serializer_class = FavoriteSerializer

    def get_queryset(self):
        note_id = self.kwargs["note_id"]
        return Favorite.objects.filter(user=self.request.user.id).filter(note=note_id)


class NoteReportView(
    mixins.CreateModelMixin, mixins.ListModelMixin, generics.GenericAPIView
):
    permission_classes = (
        permissions.IsAuthenticated,
        IsAuthorOrReadOnly,
        AlreadyPostedNoteReport,
        CanAccessFavorite,
    )
    serializer_class = NoteReportSerializer

    def perform_create(self, serializer):
        serializer.save(
            user=self.request.user, note=Note.objects.get(pk=self.kwargs["note_id"])
        )

    def get_queryset(self):
        note_id = self.kwargs["note_id"]
        return NoteReport.objects.filter(user=self.request.user.id).filter(note=note_id)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class CommentReportView(
    mixins.CreateModelMixin, mixins.ListModelMixin, generics.GenericAPIView
):
    permission_classes = (
        permissions.IsAuthenticated,
        IsAuthorOrReadOnly,
        AlreadyPostedCommentReport,
        CanAccessFavorite,
    )
    serializer_class = CommentReportSerializer

    def perform_create(self, serializer):
        serializer.save(
            user=self.request.user,
            comment=Comment.objects.get(pk=self.kwargs["comment_id"]),
        )

    def get_queryset(self):
        comment_id = self.kwargs["comment_id"]
        return CommentReport.objects.filter(user=self.request.user.id).filter(
            comment=comment_id
        )

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
