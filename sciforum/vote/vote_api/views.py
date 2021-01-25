from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework import viewsets, permissions, status
from rest_framework_jwt import authentication
from .serializers import PostVoteSerializer, PostVoteCreateSerializer, PostVoteUpdateSerializer\
    , AnswerVoteSerializer, AnswerVoteCreateSerializer, AnswerVoteUpdateSerializer, CommentVoteSerializer\
    , AnswerCommentVoteSerializer, AnswerCommentVoteCreateSerializer, AnswerCommentVoteUpdateSerializer, PostCommentVoteSerializer\
    , PostCommentVoteCreateSerializer, PostCommentVoteUpdateSerializer
from vote.models import PostVote, AnswerVote
from django_filters.rest_framework import DjangoFilterBackend
from .mixins import MultipleFieldLookupMixin
from rest_framework.response import Response
from post.models import Post
from notifications.signals import notify
from answer.models import Answer
from django.contrib.contenttypes.models import ContentType
from vote.models import CommentVote, AnswerCommentVote, PostCommentVote
from comment.models import AnswerComment, PostComment


# ANSWER VOTE
class AnswerVoteViewSet(viewsets.ModelViewSet):
    # authentication_classes = [authentication.TokenAuthentication]
    # permission_classes = [permissions.IsAuthenticated]
    queryset = AnswerVote.objects.all()
    serializer_class = AnswerVoteSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['answer', 'owner', 'voteType']
    http_method_names = ['get']


class AnswerVoteCreateview(CreateAPIView):
    authentication_classes = [authentication.JSONWebTokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = AnswerVote.objects.all()
    serializer_class = AnswerVoteCreateSerializer

    def create(self, request, *args, **kwargs):

        from_user = request.user
        action_object = Answer.objects.get(id=request.data['answer'])
        vote_type = request.data['voteType']
        to_user = action_object.owner
        content_type = ContentType.objects.get_for_model(Answer)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        if vote_type == 'LIKE':
            message = from_user.username + ' has put a like on your answer'
            if from_user.is_authenticated and from_user != to_user:
                notify.send(sender=from_user, recipient=to_user, verb=message, action_object=action_object)
        else:
            notification = to_user.notifications.filter(actor_object_id=from_user.id, action_object_content_type=content_type, action_object_object_id=action_object.id)
            # print(notification)
            try:
                notification.delete()
                # print('existing records deleted')
            except Exception as excep:
                print(excep)

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    '''
        Here I have overridden the create function in order to create or update object if it exists already
        in the model
    '''
    '''def create(self, request, *args, **kwargs):
        owner = request.data.get('owner'),
        voteType = request.data.get('voteType')
        answer = request.data.get('answer')
        #print(request.data['owner'])
        AnswerVote.objects.update_or_create(
            owner=owner,
            answer=answer,
            defaults={"voteType": voteType}
        )
        return Response(status=status.HTTP_201_CREATED)'''

    ''' below code also works fine without unique together validator '''
    '''def perform_create(self, serializer):
        owner = serializer.validated_data.get('owner'),
        voteType = serializer.validated_data.get('voteType')
        answer = serializer.validated_data.get('answer')
        print(serializer.validated_data.get('owner'))
        AnswerVote.objects.update_or_create(
            owner=owner,
            answer=answer,
            defaults={"voteType": voteType}
        )'''


class AnswerVoteUpdateView(MultipleFieldLookupMixin, UpdateAPIView):
    authentication_classes = [authentication.JSONWebTokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = AnswerVote.objects.all()
    serializer_class = AnswerVoteUpdateSerializer

    lookup_fields = ['answer', 'owner']

    def patch(self, request, *args, **kwargs):

        from_user = request.user
        action_object = self.get_object().answer
        vote_type = request.data['voteType']
        to_user = action_object.owner
        content_type = ContentType.objects.get_for_model(Answer)

        notification = to_user.notifications.filter(actor_object_id=from_user.id, action_object_content_type=content_type, action_object_object_id=action_object.id)
        try:
            notification.delete()
        except Exception as excep:
            print(excep)

        return self.partial_update(request, *args, **kwargs)


class AnswerVoteDeleteView(MultipleFieldLookupMixin, DestroyAPIView):
    authentication_classes = [authentication.JSONWebTokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = AnswerVote.objects.all()

    lookup_fields = ['answer', 'owner']


# ANSWER COMMENT VOTE
class AnswerCommentVoteViewSet(viewsets.ModelViewSet):
    # authentication_classes = [authentication.TokenAuthentication]
    # permission_classes = [permissions.IsAuthenticated]
    queryset = AnswerCommentVote.objects.all()
    serializer_class = AnswerCommentVoteSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['comment', 'owner', 'voteType']
    http_method_names = ['get']


class AnswerCommentVoteCreateview(CreateAPIView):
    authentication_classes = [authentication.JSONWebTokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = AnswerCommentVote.objects.all()
    serializer_class = AnswerCommentVoteCreateSerializer

    def create(self, request, *args, **kwargs):

        from_user = request.user
        action_object = AnswerComment.objects.get(id=request.data['comment'])
        vote_type = request.data['voteType']
        to_user = action_object.owner
        content_type = ContentType.objects.get_for_model(AnswerComment)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        if vote_type == 'LIKE':
            message = from_user.username + ' has put a like on your comment'
            if from_user.is_authenticated and from_user != to_user:
                notify.send(sender=from_user, recipient=to_user, verb=message, action_object=action_object)
        else:
            notification = to_user.notifications.filter(actor_object_id=from_user.id, action_object_content_type=content_type, action_object_object_id=action_object.id)
            try:
                notification.delete()
                # print('existing records deleted')
            except Exception as excep:
                print(excep)

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class AnswerCommentVoteUpdateView(MultipleFieldLookupMixin, UpdateAPIView):
    authentication_classes = [authentication.JSONWebTokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = AnswerCommentVote.objects.all()
    serializer_class = AnswerCommentVoteUpdateSerializer

    lookup_fields = ['comment', 'owner']

    def patch(self, request, *args, **kwargs):

        from_user = request.user
        action_object = self.get_object().comment
        vote_type = request.data['voteType']
        to_user = action_object.owner
        content_type = ContentType.objects.get_for_model(AnswerComment)

        notification = to_user.notifications.filter(actor_object_id=from_user.id, action_object_content_type=content_type, action_object_object_id=action_object.id)
        try:
            notification.delete()
        except Exception as excep:
            print(excep)

        return self.partial_update(request, *args, **kwargs)


class AnswerCommentVoteDeleteView(MultipleFieldLookupMixin, DestroyAPIView):
    authentication_classes = [authentication.JSONWebTokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = AnswerCommentVote.objects.all()

    lookup_fields = ['comment', 'owner']


# POST VOTE
class PostVoteViewSet(viewsets.ModelViewSet):
    # authentication_classes = [authentication.TokenAuthentication]
    # permission_classes = [permissions.IsAuthenticated]
    queryset = PostVote.objects.all()
    serializer_class = PostVoteSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', 'post', 'owner', 'voteType']
    http_method_names = ['get']


class PostVoteCreateview(CreateAPIView):
    authentication_classes = [authentication.JSONWebTokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = PostVote.objects.all()
    serializer_class = PostVoteCreateSerializer

    def create(self, request, *args, **kwargs):

        from_user = request.user
        action_object = Post.objects.get(id=request.data['post'])
        vote_type = request.data['voteType']
        to_user = action_object.owner
        content_type = ContentType.objects.get_for_model(Post)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        if vote_type == 'LIKE':
            message = from_user.username + ' has put a like on your question'
            if from_user.is_authenticated and from_user != to_user:
                notify.send(sender=from_user, recipient=to_user, verb=message, action_object=action_object)
        else:
            notification = to_user.notifications.filter(actor_object_id=from_user.id, action_object_content_type=content_type, action_object_object_id=action_object.id)
            # print(notification)
            try:
                notification.delete()
                # print('existing records deleted')
            except Exception as excep:
                print(excep)

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class PostVoteUpdateView(MultipleFieldLookupMixin, UpdateAPIView):
    authentication_classes = [authentication.JSONWebTokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = PostVote.objects.all()
    serializer_class = PostVoteUpdateSerializer

    lookup_fields = ['post', 'owner']

    def patch(self, request, *args, **kwargs):

        from_user = request.user
        action_object = self.get_object().post
        # vote_type = request.data['voteType']
        to_user = action_object.owner
        content_type = ContentType.objects.get_for_model(Post)

        notification = to_user.notifications.filter(actor_object_id=from_user.id, action_object_content_type=content_type, action_object_object_id=action_object.id)
        try:
            notification.delete()
        except Exception as excep:
            print(excep)

        return self.partial_update(request, *args, **kwargs)


class PostVoteDeleteView(MultipleFieldLookupMixin, DestroyAPIView):
    authentication_classes = [authentication.JSONWebTokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = PostVote.objects.all()

    lookup_fields = ['post', 'owner']


# ANSWER COMMENT VOTE
class PostCommentVoteViewSet(viewsets.ModelViewSet):
    # authentication_classes = [authentication.TokenAuthentication]
    # permission_classes = [permissions.IsAuthenticated]
    queryset = PostCommentVote.objects.all()
    serializer_class = PostCommentVoteSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['comment', 'owner', 'voteType']
    http_method_names = ['get']


class PostCommentVoteCreateview(CreateAPIView):
    authentication_classes = [authentication.JSONWebTokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = PostCommentVote.objects.all()
    serializer_class = PostCommentVoteCreateSerializer

    def create(self, request, *args, **kwargs):

        from_user = request.user
        action_object = PostComment.objects.get(id=request.data['comment'])
        vote_type = request.data['voteType']
        to_user = action_object.owner
        content_type = ContentType.objects.get_for_model(PostComment)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        if vote_type == 'LIKE':
            message = from_user.username + ' has put a like on your comment'
            if from_user.is_authenticated and from_user != to_user:
                notify.send(sender=from_user, recipient=to_user, verb=message, action_object=action_object)
        else:
            notification = to_user.notifications.filter(actor_object_id=from_user.id, action_object_content_type=content_type, action_object_object_id=action_object.id)
            # print(notification)
            try:
                notification.delete()
                # print('existing records deleted')
            except Exception as excep:
                print(excep)

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class PostCommentVoteUpdateView(MultipleFieldLookupMixin, UpdateAPIView):
    authentication_classes = [authentication.JSONWebTokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = PostCommentVote.objects.all()
    serializer_class = PostCommentVoteUpdateSerializer

    lookup_fields = ['comment', 'owner']

    def patch(self, request, *args, **kwargs):

        from_user = request.user
        action_object = self.get_object().comment
        vote_type = request.data['voteType']
        to_user = action_object.owner
        content_type = ContentType.objects.get_for_model(PostComment)

        notification = to_user.notifications.filter(actor_object_id=from_user.id, action_object_content_type=content_type, action_object_object_id=action_object.id)
        try:
            notification.delete()
        except Exception as excep:
            print(excep)

        return self.partial_update(request, *args, **kwargs)


class PostCommentVoteDeleteView(MultipleFieldLookupMixin, DestroyAPIView):
    authentication_classes = [authentication.JSONWebTokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = PostCommentVote.objects.all()

    lookup_fields = ['comment', 'owner']


'''
    SEPARATED
'''
class CommentVoteViewSet(viewsets.ModelViewSet):

    queryset = CommentVote.objects.all()
    serializer_class = CommentVoteSerializer


