from .views import NotificationViewSet, NotificationCountViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'', NotificationViewSet, basename='notifications')
router.register(r'unread/count', NotificationCountViewSet, basename='notifications_unread_count')
urlpatterns = router.urls