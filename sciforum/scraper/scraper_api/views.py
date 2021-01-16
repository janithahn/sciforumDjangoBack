from rest_framework import viewsets
from .serializers import WebinarSerializer, EventSerializer
from scraper.models import Webinar, Event


class WebinarViewSet(viewsets.ModelViewSet):

    serializer_class = WebinarSerializer
    queryset = Webinar.objects.all()

    http_method_names = ['get']


class EventViewSet(viewsets.ModelViewSet):

    serializer_class = EventSerializer
    queryset = Event.objects.all()

    http_method_names = ['get']