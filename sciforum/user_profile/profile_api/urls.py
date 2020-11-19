from django.urls import path
#from .views import PostDetailView, PostListView, PostCreateView, PostUpdateView, PostDeleteView
from user_profile.profile_api.views import ProfileViewSet
from rest_framework.routers import DefaultRouter
from .views import UserViewSet

router = DefaultRouter()
router.register(r'', ProfileViewSet, basename='profile_api')
router.register(r'users/viewset', UserViewSet, basename='users')
urlpatterns = router.urls