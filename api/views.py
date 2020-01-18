from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import generics, mixins, permissions
from .serializers import UserSerializer

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
