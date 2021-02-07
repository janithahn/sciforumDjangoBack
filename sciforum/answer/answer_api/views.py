from rest_framework.generics import CreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework import viewsets, permissions, status, filters, pagination
from rest_framework_jwt import authentication
from .serializers import AnswerSerializer, AnswerCreateSerializer, AnswerUpdateSerializer, TopAnswersSerializer
from answer.models import Answer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from notifications.signals import notify
from post.models import Post
from django.db.models import Count


class AnswersPagination(pagination.PageNumberPagination):
    page_size = 2

    def get_paginated_response(self, data):
        return Response({
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'count': self.page.paginator.count,
            'current_page': self.page.number,
            'total_pages': self.page.paginator.num_pages,
            'results': data
        })


class AnswerViewSet(viewsets.ModelViewSet):
    # authentication_classes = [authentication.TokenAuthentication]
    # permission_classes = [permissions.IsAuthenticated]
    queryset = Answer.objects.filter().annotate(vote_count=Count('answervote')).distinct()
    serializer_class = AnswerSerializer
    pagination_class = AnswersPagination
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['id', 'owner', 'postBelong']
    http_method_names = ['get']
    ordering_fields = ['vote_count', 'created_at', 'updated_at']


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

        # print(to_user.notifications.unread())

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


# Most voted answers
class TopAnswersViewSet(viewsets.ModelViewSet):
    # queryset = Post.objects.annotate(vote_count=Count('postvote')).order_by('postvote__voteType').annotate(postvote__voteType='LIKE')
    queryset = Answer.objects.filter().annotate(vote_count=Count('answervote')).distinct()
    serializer_class = TopAnswersSerializer
    http_method_names = ['get']

    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['vote_count']
