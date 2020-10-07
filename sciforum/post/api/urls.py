from django.urls import path
#from .views import PostDetailView, PostListView, PostCreateView, PostUpdateView, PostDeleteView
from post.api.views import PostViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'', PostViewSet, basename='posts')
urlpatterns = router.urls


'''urlpatterns = [
    path('', PostListView.as_view()),
    path('create/', PostCreateView.as_view()),
    path('<pk>/', PostDetailView.as_view()),
    path('<pk>/update/', PostUpdateView.as_view()),
    path('<pk>/delete/', PostDeleteView.as_view()),
]'''