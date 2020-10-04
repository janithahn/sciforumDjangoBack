from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework import viewsets, permissions, authentication, status
from user_profile.models import Profile
from .serializers import ProfileSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_auth.views import LoginView
from rest_auth.registration.views import RegisterView
from rest_auth.registration.serializers import RegisterSerializer
from django.contrib.auth.models import User
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend


class ProfileViewSet(viewsets.ModelViewSet):
    #authentication_classes = [authentication.TokenAuthentication]
    #permission_classes = [permissions.IsAuthenticated]
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    lookup_field = 'user'
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['aboutMe', 'user']
