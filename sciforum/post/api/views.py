from rest_framework.generics import ListAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework import viewsets, permissions, pagination, filters, status
from rest_framework.response import Response
from post.models import Post, Visitors, PostImages
from user_profile.models import ProfileViewerInfo
from .serializers import PostSerializer, VisitorSerializer, ProfileViewerInfoSerializer, PostUpdateSerializer\
    , PostCreateSerializer, PostTempImagesSerializer, TopPostsSerializer
from django.utils.timezone import now
from user_profile.models import Profile
from rest_framework_jwt import authentication
from .utils import get_client_ip
from django.db.models import Count, Sum
from django_filters.rest_framework import DjangoFilterBackend, FilterSet, filters as filters_for_tags
from django_filters.widgets import CSVWidget
# from rest_framework_word_filter import FullWordSearchFilter
from taggit_suggest.utils import suggest_tags
from vote.models import PostVote


# Temporary sample views to get visitors
class VisitorsListView(ListAPIView):
    queryset = Visitors.objects.all()
    serializer_class = VisitorSerializer


class ProfileViewerInfoView(ListAPIView):
    queryset = ProfileViewerInfo.objects.all()
    serializer_class = ProfileViewerInfoSerializer


# views for posts
class PostsPagination(pagination.PageNumberPagination):
    page_size = 8

    def get_paginated_response(self, data):
        return Response({
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'count': self.page.paginator.count,
            'current_page': self.page.number,
            'total_pages': self.page.paginator.num_pages,
            'results': data
        })


class TaggedPostsFilterSet(FilterSet):
    tags = filters_for_tags.BaseCSVFilter(distinct=True, widget=CSVWidget, method='filter_tags')

    class Meta:
        model = Post
        fields = ['owner', 'tags']

    def filter_tags(self, queryset, name, value):
        return queryset.filter(tags__name__in=value)


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    pagination_class = PostsPagination
    http_method_names = ['get']

    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    filter_class = TaggedPostsFilterSet
    search_fields = ['title', 'body']
    ordering_fields = ['viewCount', 'created_at']
    # filterset_fields = ['owner']
    # filter_backends = [FullWordSearchFilter]
    # word_fields = ['title', 'body']

    def retrieve(self, request, *args, **kwargs):
        postId = self.get_object().id
        postOwner = self.get_object().owner
        viewCount = 0
        totalPostViewCount = 0

        print(suggest_tags(content=['sample', 'reactjs', 'django']))

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
    authentication_classes = [authentication.JSONWebTokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
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
    authentication_classes = [authentication.JSONWebTokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = Post.objects.all()


class PostImagesViewSet(viewsets.ModelViewSet):
    queryset = PostImages.objects.all()
    serializer_class = PostTempImagesSerializer


class TopPostsViewSet(viewsets.ModelViewSet):
    # queryset = Post.objects.annotate(vote_count=Count('postvote')).order_by('postvote__voteType').annotate(postvote__voteType='LIKE')
    queryset = Post.objects.filter(postvote__voteType='LIKE').annotate(vote_count=Count('postvote')).distinct()
    pagination_class = PostsPagination
    serializer_class = TopPostsSerializer
    http_method_names = ['get']

    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['vote_count']




