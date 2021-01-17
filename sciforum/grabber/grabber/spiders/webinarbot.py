import scrapy
from ..items import WebinarsItem
import spacy


class WebinarbotSpider(scrapy.Spider):
    name = 'webinarbot'
    allowed_domains = [
        'sci.pdn.ac.lk',
        'www.fos.pdn.ac.lk',
        'sired.soc.pdn.ac.lk',
        'botsoc.soc.pdn.ac.lk',
        'csup.soc.pdn.ac.lk'
    ]
    start_urls = [
        'https://sci.pdn.ac.lk/',
        'https://csup.soc.pdn.ac.lk/',
        'https://sired.soc.pdn.ac.lk/',
        'https://botsoc.soc.pdn.ac.lk/',
        'https://www.fos.pdn.ac.lk/fosid/'
    ]

    custom_settings = {
        'DEPTH_LIMIT': 2,
    }

    items = []
    item = WebinarsItem()
    need_urls = ['meet.google', 'zoom', 'forms']

    def parse(self, response):
        tag_selector = response.xpath('//a')
        for tag in tag_selector:
            link = tag.xpath('@href').extract_first()

            for url in self.need_urls:
                if str(link).find(url) != -1:
                    parent = tag.xpath('../..')

                    while len(parent.xpath('//div')) == 0:
                        parent = parent.xpath('..')

                    texts = parent.xpath('.//text()').extract()
                    title = parent.xpath('//title/text()').extract()
                    filtered_data = self.filter_data(texts)

                    self.item['link'] = link
                    self.item['title'] = title[0]
                    self.item['texts'] = str(filtered_data).strip()
                    self.item['reference_url'] = response.url
                    yield self.item

                    self.items.append([link, str(filtered_data)])

            if link is not None and (str(link).find('download') == -1 or str(link).find('archive') == -1):
                yield response.follow(link, callback=self.parse)

    def filter_data(self, texts):

        org = []
        person = []
        date = []
        time = []
        gpe = []
        cardinal = []

        nlp = spacy.load("en_core_web_sm")
        for doc in nlp.pipe(texts, disable=["tagger", "parser"]):
            for ent in doc.ents:
                if ent.label_ == 'ORG':
                    if ent.text not in org: org.append(ent.text)
                if ent.label_ == 'PERSON':
                    if ent.text not in person: person.append(ent.text)
                if ent.label_ == 'DATE':
                    if ent.text not in date: date.append(ent.text)
                if ent.label_ == 'TIME':
                    if ent.text not in time: time.append(ent.text)
                if ent.label_ == 'GPE':
                    if ent.text not in gpe: gpe.append(ent.text)
                if ent.label_ == 'CARDINAL':
                    if ent.text not in cardinal: cardinal.append(ent.text)

        return_item = {
            'ORG': org,
            'PERSON': person,
            'DATE': date,
            'TIME': time,
            'GPE': gpe,
            'CARDINAL': cardinal
        }

        def join_list(lst):
            if not lst:
                return None
            else:
                return ', '.join(lst)

        sentences = [join_list(org), join_list(gpe), join_list(date), join_list(time), join_list(person)]
        sentences = [sent for sent in sentences if sent is not None]

        return_sentence = join_list(sentences)

        return return_sentence
