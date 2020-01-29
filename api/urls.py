from django.urls import path
from rest_framework.authtoken import views
from .views import UserView, NoteView, NoteDetailView, NoteFileView, NoteFileDetailView

urlpatterns = [
    path("login/", views.obtain_auth_token),
    path("user/", UserView.as_view()),
    path("notes/", NoteView.as_view()),
    path("notes/<int:pk>/", NoteDetailView.as_view()),
    path("notes/<int:note_id>/files", NoteFileView.as_view()),
    path("notes/<int:note_id>/files/<int:index>", NoteFileDetailView.as_view()),
]
