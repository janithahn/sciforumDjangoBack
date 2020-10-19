from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework import viewsets, permissions, status
from rest_framework_jwt import authentication
from .serializers import PostVoteSerializer, PostVoteCreateSerializer, PostVoteUpdateSerializer\
    , AnswerVoteSerializer, AnswerVoteCreateSerializer, AnswerVoteUpdateSerializer
from vote.models import PostVote, AnswerVote
from django_filters.rest_framework import DjangoFilterBackend
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
    filterset_fields = ['id', 'answer', 'owner', 'voteType']
    http_method_names = ['get']

class AnswerVoteCreateview(CreateAPIView):
    #authentication_classes = [authentication.JSONWebTokenAuthentication]
    #permission_classes = [permissions.IsAuthenticated]
    queryset = AnswerVote.objects.all()
    serializer_class = AnswerVoteCreateSerializer

    '''def create(self, request, *args, **kwargs):
        print(request.data['answer'])
        print(request.user)
        obj = None

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            obj = AnswerVote.objects.get(answer=request.data['answer'], voteType=request.data['voteType'], owner=request.data['owner'])
            print('YES')
        except Exception as excep:
            if(excep == AnswerVote.DoesNotExist):
                print('YES')
                self.perform_create(serializer)
                headers = self.get_success_headers(serializer.data)
                return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

        return Response(None)'''

class AnswerVoteUpdateView(UpdateAPIView):
    #authentication_classes = [authentication.JSONWebTokenAuthentication]
    #permission_classes = [permissions.IsAuthenticated]
    queryset = AnswerVote.objects.all()
    serializer_class = AnswerVoteUpdateSerializer

class AnswerVoteDeleteView(DestroyAPIView):
    #authentication_classes = [authentication.JSONWebTokenAuthentication]
    #permission_classes = [permissions.IsAuthenticated]
    queryset = AnswerVote.objects.all()


