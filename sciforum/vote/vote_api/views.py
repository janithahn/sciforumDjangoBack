from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework import viewsets, permissions, status
from rest_framework_jwt import authentication
from .serializers import PostVoteSerializer, PostVoteCreateSerializer, PostVoteUpdateSerializer\
    , AnswerVoteSerializer, AnswerVoteCreateSerializer, AnswerVoteUpdateSerializer
from vote.models import PostVote, AnswerVote
from django_filters.rest_framework import DjangoFilterBackend
from .mixins import MultipleFieldLookupMixin
from rest_framework.response import Response

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
    filterset_fields = ['answer', 'owner', 'voteType']
    #http_method_names = ['get']

    def create(self, validated_data):
        answer, created = AnswerVote.objects.update_or_create(
            answer=validated_data.data.get('answer', None),
            owner=validated_data.data.get('owner', None),
        )
        return answer


class AnswerVoteCreateview(CreateAPIView):
    #authentication_classes = [authentication.JSONWebTokenAuthentication]
    #permission_classes = [permissions.IsAuthenticated]
    queryset = AnswerVote.objects.all()
    serializer_class = AnswerVoteCreateSerializer

class AnswerVoteUpdateView(MultipleFieldLookupMixin, UpdateAPIView):
    #authentication_classes = [authentication.JSONWebTokenAuthentication]
    #permission_classes = [permissions.IsAuthenticated]
    queryset = AnswerVote.objects.all()
    serializer_class = AnswerVoteUpdateSerializer

    lookup_fields = ['answer', 'owner']

class AnswerVoteDeleteView(MultipleFieldLookupMixin, DestroyAPIView):
    authentication_classes = [authentication.JSONWebTokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = AnswerVote.objects.all()

    lookup_fields = ['answer', 'owner']


