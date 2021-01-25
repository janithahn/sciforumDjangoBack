from rest_framework import viewsets, permissions, status
from rest_framework_jwt import authentication
from .serializers import AnswerCommentSerializer, PostCommentSerializer, PostCommentMentionsSerializer, AnswerCommentMentionsSerializer
from comment.models import PostComment, AnswerComment, PostCommentMentions, AnswerCommentMentions
from django_filters.rest_framework import DjangoFilterBackend
# from .mixins import MultipleFieldLookupMixin
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

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        from_user = request.user
        action_object = AnswerComment.objects.get(id=serializer.data['id'])
        message = from_user.username + ' has put a comment on your answer'
        to_user = Answer.objects.get(id=request.data['answer']).owner

        if from_user.is_authenticated and from_user != to_user:
            notify.send(sender=from_user, recipient=to_user, verb=message, action_object=action_object)

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        ''' deleting mention notifications '''
        mentions = AnswerCommentMentions.objects.filter(comment=instance)
        from_user = instance.owner
        action_object = instance
        content_type = ContentType.objects.get_for_model(AnswerComment)
        for mention in mentions:
            to_user = mention.user
            try:
                notification = to_user.notifications.filter(actor_object_id=from_user.id, action_object_content_type=content_type, action_object_object_id=action_object.id)
                notification.delete()
            except Exception as excep:
                print(excep)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        from_user = instance.owner
        action_object = instance
        to_user = instance.post.owner
        content_type = ContentType.objects.get_for_model(AnswerComment)

        notification = to_user.notifications.filter(actor_object_id=from_user.id, action_object_content_type=content_type, action_object_object_id=action_object.id)
        try:
            notification.delete()
        except Exception as excep:
            print(excep)
        instance.delete()


class AnswerCommentMentionsViewSet(viewsets.ModelViewSet):
    queryset = AnswerCommentMentions.objects.all()
    serializer_class = AnswerCommentMentionsSerializer


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

    '''def get_queryset(self):
        comments_qs = PostComment.objects.all()
        mentions_qs = PostCommentMentions.objects.all()

        return comments_qs.union(mentions_qs, all=True)'''

    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        from_user = request.user
        action_object = PostComment.objects.get(id=serializer.data['id'])
        message = from_user.username + ' has put a comment on your post'
        to_user = Post.objects.get(id=request.data['post']).owner

        if from_user.is_authenticated and from_user != to_user:
            notify.send(sender=from_user, recipient=to_user, verb=message, action_object=action_object)

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        ''' deleting mention notifications '''
        mentions = PostCommentMentions.objects.filter(comment=instance)
        from_user = instance.owner
        action_object = instance
        content_type = ContentType.objects.get_for_model(PostComment)
        for mention in mentions:
            to_user = mention.user
            try:
                notification = to_user.notifications.filter(actor_object_id=from_user.id, action_object_content_type=content_type, action_object_object_id=action_object.id)
                notification.delete()
            except Exception as excep:
                print(excep)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        from_user = instance.owner
        action_object = instance
        to_user = instance.post.owner
        content_type = ContentType.objects.get_for_model(PostComment)
        ''' deleting comment notifications for the user '''
        notification = to_user.notifications.filter(actor_object_id=from_user.id, action_object_content_type=content_type, action_object_object_id=action_object.id)
        try:
            notification.delete()
        except Exception as excep:
            print(excep)
        instance.delete()


class PostCommentMentionsViewSet(viewsets.ModelViewSet):
    queryset = PostCommentMentions.objects.all()
    serializer_class = PostCommentMentionsSerializer



