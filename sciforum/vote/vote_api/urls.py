from django.urls import path
#from .views import PostDetailView, PostListView, PostCreateView, PostUpdateView, PostDeleteView
from .views import PostVoteViewSet, AnswerVoteViewSet, PostCommentVoteViewSet, AnswerCommentVoteViewSet, CommentVoteViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(r'postvote', PostVoteViewSet, basename='post_vote_api')
router.register(r'answervote', AnswerVoteViewSet, basename='answer_vote_api')
router.register(r'postcommentvote', PostCommentVoteViewSet, basename='post_comment_vote_api')
router.register(r'answercommentvote', AnswerCommentVoteViewSet, basename='answer_comment_vote_api')
router.register(r'comment_vote', CommentVoteViewSet, basename='comment_vote_api')

urlpatterns = router.urls