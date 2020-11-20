from rest_framework.generics import ListAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework import viewsets, permissions, pagination, status
from rest_framework.response import Response
from post.models import Post, Visitors
from user_profile.models import ProfileViewerInfo
from .serializers import PostSerializer, VisitorSerializer, ProfileViewerInfoSerializer, PostUpdateSerializer, PostCreateSerializer
from django.utils.timezone import now
from user_profile.models import Profile
from rest_framework_jwt import authentication
from .utils import get_client_ip
from django.db.models import Count, Sum
from rest_framework import filters
# from rest_framework_word_filter import FullWordSearchFilter
from taggit_suggest.utils import suggest_tags

# Temporary sample views to get visitors
class VisitorsListView(ListAPIView):
    queryset = Visitors.objects.all()
    serializer_class = VisitorSerializer

class ProfileViewerInfoView(ListAPIView):
    queryset = ProfileViewerInfo.objects.all()
    serializer_class = ProfileViewerInfoSerializer

#views for posts
class PostsPagination(pagination.PageNumberPagination):
    page_size = 5

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    pagination_class = PostsPagination
    http_method_names = ['get']

    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'body']
    ordering_fields = ['viewCount', 'created_at']
    # filter_backends = [FullWordSearchFilter]
    # word_fields = ['title', 'body']

    def retrieve(self, request, *args, **kwargs):
        # viewCounter = Visitors.objects.values('post_id').annotate(viewCount=Count('visitorIp', distinct=True))
        postId = self.get_object().id
        postOwner = self.get_object().owner
        viewCount = 0
        totalPostViewCount = 0

        print(suggest_tags(content='react text with django drf text here'))

        try:
            viewCount = Visitors.objects.filter(post_id=postId).values('post_id').annotate(viewCount=Count('visitorIp', distinct=True))[0]['viewCount']
        except Exception as exep:
            print(exep)

        newVisitor = Visitors(post=self.get_object(), visitorIp=get_client_ip(request), visitDate=now())
        newVisitor.save()

        try:
            totalPostViewCount = Post.objects.filter(owner=postOwner).aggregate(totalPostViewCount=Sum('viewCount'))['totalPostViewCount']
        except Exception as exep:
            print(exep)

        print(totalPostViewCount)
        profileObj = Profile.objects.get(user=postOwner)
        profileObj.postViews = totalPostViewCount
        profileObj.save(update_fields=('postViews', ))

        obj = self.get_object()
        obj.viewCount = viewCount
        obj.save(update_fields=('viewCount', ))
        return super().retrieve(request, *args, **kwargs)

class PostCreateview(CreateAPIView):
    #authentication_classes = [authentication.JSONWebTokenAuthentication]
    #permission_classes = [permissions.IsAuthenticated]
    queryset = Post.objects.all()
    serializer_class = PostCreateSerializer

    '''def perform_create(self, serializer):
        instance = serializer.save()
        if 'tags' in self.request.data:
            # instance.tags = suggest_tags(self.request.data['tags'])
            instance.tags = self.request.data['tags']
            instance.save()
            print(instance.tags)'''


class PostUpdateView(UpdateAPIView):
    authentication_classes = [authentication.JSONWebTokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = Post.objects.all()
    serializer_class = PostUpdateSerializer

class PostDeleteView(DestroyAPIView):
    # authentication_classes = [authentication.JSONWebTokenAuthentication]
    # permission_classes = [permissions.IsAuthenticated]
    queryset = Post.objects.all()

