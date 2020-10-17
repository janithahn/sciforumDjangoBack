from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework import viewsets, permissions, status
from rest_framework_jwt import authentication
from .serializers import AnswerSerializer, AnswerCreateSerializer, AnswerUpdateSerializer
from answer.models import Answer
from django_filters.rest_framework import DjangoFilterBackend


class AnswerViewSet(viewsets.ModelViewSet):
    #authentication_classes = [authentication.TokenAuthentication]
    #permission_classes = [permissions.IsAuthenticated]
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', 'owner', 'postBelong']
    http_method_names = ['get']

class AnswerCreateview(CreateAPIView):
    #authentication_classes = [authentication.JSONWebTokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = Answer.objects.all()
    serializer_class = AnswerCreateSerializer

class AnswerUpdateView(UpdateAPIView):
    authentication_classes = [authentication.JSONWebTokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = Answer.objects.all()
    serializer_class = AnswerUpdateSerializer

class AnswerDeleteView(DestroyAPIView):
    authentication_classes = [authentication.JSONWebTokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = Answer.objects.all()


