from .views import AnswerViewSet, TopAnswersViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'', AnswerViewSet, basename='answer_api')
router.register(r'top/answers', TopAnswersViewSet, basename='answers')
urlpatterns = router.urls