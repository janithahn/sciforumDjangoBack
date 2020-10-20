from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework import viewsets, permissions, status
from rest_framework_jwt import authentication
from .serializers import PostVoteSerializer, PostVoteCreateSerializer, PostVoteUpdateSerializer\
    , AnswerVoteSerializer, AnswerVoteCreateSerializer, AnswerVoteUpdateSerializer
from vote.models import PostVote, AnswerVote
from django_filters.rest_framework import DjangoFilterBackend
from .mixins import MultipleFieldLookupMixin
from rest_framework.response import Response

#ANSWER VOTE
class AnswerVoteViewSet(viewsets.ModelViewSet):
    #authentication_classes = [authentication.TokenAuthentication]
    #permission_classes = [permissions.IsAuthenticated]
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

    '''
        Here I have overridden the create function in order to create or update object if exists already
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

class AnswerVoteDeleteView(MultipleFieldLookupMixin, DestroyAPIView):
    authentication_classes = [authentication.JSONWebTokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = AnswerVote.objects.all()

    lookup_fields = ['answer', 'owner']

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

class PostVoteUpdateView(MultipleFieldLookupMixin, UpdateAPIView):
    #authentication_classes = [authentication.JSONWebTokenAuthentication]
    #permission_classes = [permissions.IsAuthenticated]
    queryset = PostVote.objects.all()
    serializer_class = PostVoteUpdateSerializer

    lookup_fields = ['post', 'owner']

class PostVoteDeleteView(MultipleFieldLookupMixin, DestroyAPIView):
    #authentication_classes = [authentication.JSONWebTokenAuthentication]
    #permission_classes = [permissions.IsAuthenticated]
    queryset = PostVote.objects.all()

    lookup_fields = ['post', 'owner']

