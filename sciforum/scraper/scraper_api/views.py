from rest_framework import viewsets
from .serializers import WebinarSerializer, EventSerializer
from scraper.models import Webinar, Event
from rest_framework import pagination, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response


class EventsPagination(pagination.PageNumberPagination):
    page_size = 8

    def get_paginated_response(self, data):
        return Response({
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'count': self.page.paginator.count,
            'current_page': self.page.number,
            'total_pages': self.page.paginator.num_pages,
            'results': data
        })


class WebinarViewSet(viewsets.ModelViewSet):

    serializer_class = WebinarSerializer
    queryset = Webinar.objects.all()
    pagination_class = EventsPagination
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]

    http_method_names = ['get']


class EventViewSet(viewsets.ModelViewSet):

    serializer_class = EventSerializer
    queryset = Event.objects.all()
    pagination_class = EventsPagination
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]

    http_method_names = ['get']