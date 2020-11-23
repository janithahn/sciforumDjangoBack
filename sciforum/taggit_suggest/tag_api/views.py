from rest_framework.generics import ListAPIView
from rest_framework import viewsets, permissions, status
from rest_framework_jwt import authentication
from .serializers import TagSerializer
from taggit.models import Tag

class TagListView(ListAPIView):
    # authentication_classes = [authentication.JSONWebTokenAuthentication]
    # permission_classes = [permissions.IsAuthenticated]
    queryset = Tag.objects.all()
    serializer_class = TagSerializer