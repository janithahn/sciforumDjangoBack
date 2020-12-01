from django.urls import path
#from .views import PostDetailView, PostListView, PostCreateView, PostUpdateView, PostDeleteView
from user_profile.profile_api.views import ProfileViewSet, UserViewSet, UserEmploymentViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(r'', ProfileViewSet, basename='profile_api')
router.register(r'users/viewset', UserViewSet, basename='users')
router.register(r'user_employment/viewset', UserEmploymentViewSet, 'user_employment')

urlpatterns = router.urls
