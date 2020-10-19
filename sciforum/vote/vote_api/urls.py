from django.urls import path
#from .views import PostDetailView, PostListView, PostCreateView, PostUpdateView, PostDeleteView
from .views import PostVoteViewSet, AnswerVoteViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'postvote', PostVoteViewSet, basename='post_vote_api')
router.register(r'answervote', AnswerVoteViewSet, basename='answer_vote_api')
urlpatterns = router.urls