from rest_framework.routers import DefaultRouter
from scraper.scraper_api.views import WebinarViewSet, EventViewSet

router = DefaultRouter()

router.register(r'webinars', WebinarViewSet, basename='webinars')
router.register(r'events', EventViewSet, basename='events')

urlpatterns = router.urls