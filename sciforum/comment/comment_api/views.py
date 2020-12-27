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

    authentication_classes = [authentication.JSONWebTokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    queryset = AnswerComment.objects.all()
    serializer_class = AnswerCommentSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['answer', 'post', 'owner']
    http_method_names = ['get', 'post', 'patch', 'delete']

    def create(self, request, *args, **kwargs):

        from_user = request.user
        action_object = Answer.objects.get(id=request.data['answer'])
        message = from_user.username + ' has put a comment on your answer'
        to_user = action_object.owner

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        if from_user.is_authenticated:
            notify.send(sender=from_user, recipient=to_user, verb=message, action_object=action_object)

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_destroy(self, instance):
        from_user = instance.owner
        action_object = instance.post
        to_user = instance.post.owner
        content_type = ContentType.objects.get_for_model(Answer)

        notification = to_user.notifications.filter(actor_object_id=from_user.id, action_object_content_type=content_type, action_object_object_id=action_object.id)
        try:
            notification.delete()
        except Exception as excep:
            print(excep)
        instance.delete()


# POST
class PostCommentViewSet(viewsets.ModelViewSet):

    queryset = PostComment.objects.all()
    serializer_class = PostCommentSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['post', 'owner', 'id']
    http_method_names = ['get']


class PostCommentCreateViewSet(viewsets.ModelViewSet):

    authentication_classes = [authentication.JSONWebTokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    queryset = PostComment.objects.all()
    serializer_class = PostCommentSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['post', 'owner', 'id']
    http_method_names = ['get', 'post', 'patch', 'delete']

    def create(self, request, *args, **kwargs):

        from_user = request.user
        action_object = Post.objects.get(id=request.data['post'])
        message = from_user.username + ' has put a comment on your post'
        to_user = action_object.owner

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        if from_user.is_authenticated:
            notify.send(sender=from_user, recipient=to_user, verb=message, action_object=action_object)

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_destroy(self, instance):
        from_user = instance.owner
        action_object = instance.post
        to_user = instance.post.owner
        content_type = ContentType.objects.get_for_model(Post)

        notification = to_user.notifications.filter(actor_object_id=from_user.id, action_object_content_type=content_type, action_object_object_id=action_object.id)
        try:
            notification.delete()
        except Exception as excep:
            print(excep)
        instance.delete()


