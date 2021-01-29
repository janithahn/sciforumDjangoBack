# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy_djangoitem import DjangoItem
from scraper.models import Event, Webinar


class EventsItem(DjangoItem):
    django_model = Event


class WebinarsItem(DjangoItem):
    django_model = Webinar