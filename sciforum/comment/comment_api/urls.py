from django.urls import path
from .views import PostCommentViewSet, AnswerCommentViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'post_comment', PostCommentViewSet, basename='post_comment_api')
router.register(r'answer_comment', AnswerCommentViewSet, basename='answer_comment_api')
urlpatterns = router.urls