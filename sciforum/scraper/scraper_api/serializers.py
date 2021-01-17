from rest_framework import serializers
from scraper.models import Webinar, Event


class WebinarSerializer(serializers.ModelSerializer):

    class Meta:
        model = Webinar
        fields = ['id', 'title', 'link', 'texts', 'reference_url', 'created_at']


class EventSerializer(serializers.ModelSerializer):

    class Meta:
        model = Event
        fields = ['id', 'title', 'link', 'sentences', 'created_at']