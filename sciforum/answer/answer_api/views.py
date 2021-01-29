from rest_framework.generics import CreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework import viewsets, permissions, status
from rest_framework_jwt import authentication
from .serializers import AnswerSerializer, AnswerCreateSerializer, AnswerUpdateSerializer
from answer.models import Answer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from notifications.signals import notify
from post.models import Post


class AnswerViewSet(viewsets.ModelViewSet):
    # authentication_classes = [authentication.TokenAuthentication]
    # permission_classes = [permissions.IsAuthenticated]
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', 'owner', 'postBelong']
    http_method_names = ['get']


class AnswerCreateview(CreateAPIView):
    authentication_classes = [authentication.JSONWebTokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = Answer.objects.all()
    serializer_class = AnswerCreateSerializer

    def create(self, request, *args, **kwargs):

        from_user = request.user
        action_object = Post.objects.get(id=request.data['postBelong'])
        message = from_user.username + ' has put an answer to your question'
        to_user = action_object.owner

        #print(to_user.notifications.unread())

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        if from_user.is_authenticated and from_user != to_user:
            notify.send(sender=from_user, recipient=to_user, verb=message, action_object=action_object)

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class AnswerUpdateView(UpdateAPIView):
    authentication_classes = [authentication.JSONWebTokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = Answer.objects.all()
    serializer_class = AnswerUpdateSerializer


class AnswerDeleteView(DestroyAPIView):
    authentication_classes = [authentication.JSONWebTokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = Answer.objects.all()
