from django.urls import path
from rest_framework.authtoken import views
from .views import (
    UserView,
    NoteView,
    NoteDetailView,
    NoteFileView,
    NoteFileDetailView,
    UniversityView,
    UniversityDetailView,
    RatingView,
    RatingDetailView,
    SelfView,
    SelfFileView,
    CommentView,
    CommentDetailView,
)

urlpatterns = [
    path("login/", views.obtain_auth_token),
    path("user/", SelfView.as_view()),
    path("user/files", SelfFileView.as_view()),
    path("users/", UserView.as_view()),
    path("notes/", NoteView.as_view()),
    path("notes/<int:pk>/", NoteDetailView.as_view()),
    path("notes/<int:note_id>/files", NoteFileView.as_view()),
    path("notes/<int:note_id>/files/<int:index>", NoteFileDetailView.as_view()),
    path("notes/<int:note_id>/ratings", RatingView.as_view()),
    path("notes/<int:note_id>/ratings/<int:pk>", RatingDetailView.as_view()),
    path("notes/<int:note_id>/comments", CommentView.as_view()),
    path("notes/<int:note_id>/comments/<int:pk>", CommentDetailView.as_view()),
    path("universities/", UniversityView.as_view()),
    path("universities/<str:name>/", UniversityDetailView.as_view()),
]
