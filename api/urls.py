from django.urls import path
from rest_framework.authtoken import views
from .views import UserView

urlpatterns = [
    path('login/', views.obtain_auth_token),
    path('user/', UserView.as_view()),
]
