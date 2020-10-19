from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework import viewsets, permissions, status
from rest_framework_jwt import authentication
from .serializers import PostVoteSerializer, PostVoteCreateSerializer, PostVoteUpdateSerializer\
    , AnswerVoteSerializer, AnswerVoteCreateSerializer, AnswerVoteUpdateSerializer
from vote.models import PostVote, AnswerVote
from django_filters.rest_framework import DjangoFilterBackend

# POST VOTE
class PostVoteViewSet(viewsets.ModelViewSet):
    #authentication_classes = [authentication.TokenAuthentication]
    #permission_classes = [permissions.IsAuthenticated]
    queryset = PostVote.objects.all()
    serializer_class = PostVoteSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', 'post', 'owner', 'voteType']
    http_method_names = ['get']

class PostVoteCreateview(CreateAPIView):
    #authentication_classes = [authentication.JSONWebTokenAuthentication]
    #permission_classes = [permissions.IsAuthenticated]
    queryset = PostVote.objects.all()
    serializer_class = PostVoteCreateSerializer

class PostVoteUpdateView(UpdateAPIView):
    #authentication_classes = [authentication.JSONWebTokenAuthentication]
    #permission_classes = [permissions.IsAuthenticated]
    queryset = PostVote.objects.all()
    serializer_class = PostVoteUpdateSerializer

class PostVoteDeleteView(DestroyAPIView):
    #authentication_classes = [authentication.JSONWebTokenAuthentication]
    #permission_classes = [permissions.IsAuthenticated]
    queryset = PostVote.objects.all()

#ANSWER VOTE
class AnswerVoteViewSet(viewsets.ModelViewSet):
    #authentication_classes = [authentication.TokenAuthentication]
    #permission_classes = [permissions.IsAuthenticated]
    queryset = AnswerVote.objects.all()
    serializer_class = AnswerVoteSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', 'answer', 'owner', 'voteType']
    http_method_names = ['get']

class AnswerVoteCreateview(CreateAPIView):
    #authentication_classes = [authentication.JSONWebTokenAuthentication]
    #permission_classes = [permissions.IsAuthenticated]
    queryset = AnswerVote.objects.all()
    serializer_class = AnswerVoteCreateSerializer

class AnswerVoteUpdateView(UpdateAPIView):
    #authentication_classes = [authentication.JSONWebTokenAuthentication]
    #permission_classes = [permissions.IsAuthenticated]
    queryset = AnswerVote.objects.all()
    serializer_class = AnswerVoteUpdateSerializer

class AnswerVoteDeleteView(DestroyAPIView):
    #authentication_classes = [authentication.JSONWebTokenAuthentication]
    #permission_classes = [permissions.IsAuthenticated]
    queryset = AnswerVote.objects.all()


