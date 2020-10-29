from django.urls import path
#from .views import PostDetailView, PostListView, PostCreateView, PostUpdateView, PostDeleteView
from .views import AnswerViewSet, NotificationViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'', AnswerViewSet, basename='answer_api')
router.register(r'notifications/list', NotificationViewSet, basename='notifications')
urlpatterns = router.urls