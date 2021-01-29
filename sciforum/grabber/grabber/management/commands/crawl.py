from django.core.management.base import BaseCommand
from grabber.grabber.spiders.eventbot import EventbotSpider
from grabber.grabber.spiders.webinarbot import WebinarbotSpider
from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from grabber.grabber import settings as grabber_settings
from scrapy.utils.project import get_project_settings


class Command(BaseCommand):
  help = "Release the spiders"

  def handle(self, *args, **options):
      crawler_settings = Settings()
      crawler_settings.setmodule(grabber_settings)
      process = CrawlerProcess(settings=crawler_settings)

      process.crawl(WebinarbotSpider)
      process.start()