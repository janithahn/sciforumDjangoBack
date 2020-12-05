from django.urls import path
from .views import PostCommentViewSet, AnswerCommentViewSet, PostCommentCreateViewSet, AnswerCommentCreateViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(r'post_comment', PostCommentViewSet, basename='post_comment_api')
router.register(r'answer_comment', AnswerCommentViewSet, basename='answer_comment_api')

router.register(r'post_comment_create', PostCommentCreateViewSet, basename='post_comment_create_api')
router.register(r'answer_comment_create', AnswerCommentCreateViewSet, basename='answer_comment_create_api')

urlpatterns = router.urls