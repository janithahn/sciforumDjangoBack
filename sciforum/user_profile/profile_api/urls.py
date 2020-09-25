from django.urls import path
#from .views import PostDetailView, PostListView, PostCreateView, PostUpdateView, PostDeleteView
from user_profile.profile_api.views import ProfileViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'', ProfileViewSet, basename='user_profile')
urlpatterns = router.urls


'''urlpatterns = [
    path('', PostListView.as_view()),
    path('create/', PostCreateView.as_view()),
    path('<pk>/', PostDetailView.as_view()),
    path('<pk>/update/', PostUpdateView.as_view()),
    path('<pk>/delete/', PostDeleteView.as_view()),
]'''