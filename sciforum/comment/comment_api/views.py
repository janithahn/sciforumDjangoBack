from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework import viewsets, permissions, status
from rest_framework_jwt import authentication
from .serializers import AnswerCommentSerializer, PostCommentSerializer
from comment.models import PostComment, AnswerComment
from django_filters.rest_framework import DjangoFilterBackend
from .mixins import MultipleFieldLookupMixin
from rest_framework.response import Response
from post.models import Post
from notifications.signals import notify
from answer.models import Answer
from django.contrib.contenttypes.models import ContentType


# ANSWER
class AnswerCommentViewSet(viewsets.ModelViewSet):

    queryset = AnswerComment.objects.all()
    serializer_class = AnswerCommentSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['answer', 'post', 'owner']
    http_method_names = ['get']


class AnswerCommentCreateViewSet(viewsets.ModelViewSet):

    # authentication_classes = [authentication.TokenAuthentication]
    # permission_classes = [permissions.IsAuthenticated]

    queryset = AnswerComment.objects.all()
    serializer_class = AnswerCommentSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['answer', 'post', 'owner']
    http_method_names = ['get', 'post', 'patch', 'delete']


# POST
class PostCommentViewSet(viewsets.ModelViewSet):

    queryset = PostComment.objects.all()
    serializer_class = PostCommentSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['post', 'owner', 'id']
    http_method_names = ['get']


class PostCommentCreateViewSet(viewsets.ModelViewSet):

    # authentication_classes = [authentication.TokenAuthentication]
    # permission_classes = [permissions.IsAuthenticated]

    queryset = PostComment.objects.all()
    serializer_class = PostCommentSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['post', 'owner', 'id']
    http_method_names = ['get', 'post', 'patch', 'delete']

