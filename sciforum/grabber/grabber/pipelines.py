# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import pandas as pd
from scrapy.exceptions import DropItem
from itemadapter import ItemAdapter
import json
from .items import WebinarsItem, EventsItem
from scraper.models import Webinar, Event
import spacy
import re


class WebinargrabberPipeline:

    def process_item(self, item, spider):
        return item


class DataframePipeline:

    def close_spider(self, spider):
        if spider.name == 'webinarbot':
            df = pd.DataFrame(spider.items, columns=['Link', 'Filtered Data'])
            df = df.set_index('Link').drop_duplicates()

            print(df)
            df.to_csv('webinars.csv')

        return None


class DuplicatesPipeline:

    def __init__(self):
        self.ids_seen = set()

    def process_item(self, item, spider):
        if spider.name == 'webinarbot':
            adapter = ItemAdapter(item)
            if adapter['link'] in self.ids_seen:
                raise DropItem(f"Duplicate item found: {item!r}")
            else:
                self.ids_seen.add(adapter['link'])
                return item


class EventDuplicatesPipeline:

    def __init__(self):
        self.ids_seen = set()

    def open_spider(self, spider):
        if spider.name == 'webinarbot':
            self.file = open('webinars.json', 'w')
        elif spider.name == 'eventbot':
            self.file = open('events.json', 'w')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        # adapter = ItemAdapter(item)

        if spider.name == 'eventbot':
            texts = spider.raw_texts
            adapter = EventsItem(item)
            nlp = spacy.load("en_core_web_sm")

            if adapter['title'] in self.ids_seen:
                raise DropItem(f"Duplicate item found: {item!r}")
            else:
                if 'event' in adapter['link'] or 'news' in adapter['link']:
                    self.ids_seen.add(adapter['title'])

                    avoid_list = [adapter['title'], 'Search this site', 'Report abuse', 'Report Abuse', 'report abuse']

                    doc = nlp(texts)
                    sentences = list(doc.sents)
                    sentences = [" ".join(re.split(r"\s{2,}", str(sent))) for sent in sentences]
                    big_sentence = ''

                    for sentence in sentences:
                        for avoid in avoid_list:
                            if avoid in sentence:
                                sentence = sentence.strip().replace(avoid, '')
                        big_sentence += sentence.strip() + ' '

                    adapter['sentences'] = big_sentence.strip()

                    line = json.dumps(dict(adapter)) + "\n"
                    self.file.write(line)

                    if Event.objects.filter(title=adapter['title']).exists():
                        adapter.update()
                    else:
                        adapter.save()
                    return item
                return None

        elif spider.name == 'webinarbot':
            adapter = WebinarsItem(item)

            if adapter['link'] in self.ids_seen:
                raise DropItem(f"Duplicate item found: {item!r}")
            else:
                self.ids_seen.add(adapter['link'])

                line = json.dumps(dict(adapter)) + "\n"
                self.file.write(line)

                if Webinar.objects.filter(link=adapter['link']).exists():
                    adapter.update()
                else:
                    adapter.save()
                return item