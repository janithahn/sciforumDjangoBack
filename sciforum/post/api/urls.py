from django.urls import path
from .views import PostImagesViewSet
from post.api.views import PostViewSet, TopPostsViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'', PostViewSet, basename='posts')
router.register(r'images/viewset', PostImagesViewSet, basename='images')
router.register(r'top/posts', TopPostsViewSet, basename='posts')
# router.register(r'users/viewset', UserViewSet, basename='users')
urlpatterns = router.urls


'''urlpatterns = [
    path('', PostListView.as_view()),
    path('create/', PostCreateView.as_view()),
    path('<pk>/', PostDetailView.as_view()),
    path('<pk>/update/', PostUpdateView.as_view()),
    path('<pk>/delete/', PostDeleteView.as_view()),
]'''