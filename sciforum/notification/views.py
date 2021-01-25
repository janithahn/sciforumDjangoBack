from notifications.models import Notification
from .serializers import NotificationSerializer, NotificationCountSerializer
from rest_framework import viewsets, permissions
from rest_framework_jwt import authentication
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response


class NotificationViewSet(viewsets.ModelViewSet):
    # authentication_classes = [authentication.JSONWebTokenAuthentication]
    # permission_classes = [permissions.IsAuthenticated]
    serializer_class = NotificationSerializer
    queryset = Notification.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', 'recipient', 'unread']
    http_method_names = ['get', 'delete', 'patch']

    def list(self, request, *args, **kwargs):

        '''user = User.objects.get(pk=1)
        notifications = user.notifications.read()
        notifications.mark_all_as_unread()
        print(notifications)'''

        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class NotificationCountViewSet(viewsets.ReadOnlyModelViewSet):
    authentication_classes = [authentication.JSONWebTokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = NotificationCountSerializer
    queryset = Notification.objects.unread()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['recipient', 'unread']
    http_method_names = ['get']