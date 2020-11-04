from .views import AnswerViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'', AnswerViewSet, basename='answer_api')
urlpatterns = router.urls