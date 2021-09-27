import scrapy
from urllib.parse import urljoin
from src.sources.sources import *
import pandas as pd
from src.scraper.items import *
from src.utilities.summarizer import summarize_english_news
from src.utilities.mongo import MongoDB
from src.utilities.translate import translate
from src.sources.languages import languages
from datetime import datetime
from scrapy.http import Request
class NewsSpider(scrapy.Spider):
    name = 'news'

    def __init__(self, source_information):
        self.source_id = source_information.get("_id")
        self.url = source_information.get("url")
        self.topic = source_information.get("topic")
        self.source_url = source_information.get("source_url")
        self.page_xpath = source_information.get("page_xpath")
        self.news_xpath = source_information.get("news_xpath")
        self.title_xpath = source_information.get("title_xpath")
        self.description_xpath = source_information.get("description_xpath")
        self.image_xpath = source_information.get("image_xpath",[])
        self.language = source_information.get("language")
        self.time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        self.p = ""
    def start_requests(self):
        yield scrapy.Request(url=self.url, callback=self.parse)

    def parse(self, response):
        print("hererer")
        pages = response.xpath(self.page_xpath).extract()
        print(pages)
        for page in pages:
            page = urljoin(self.url,page)
            yield scrapy.Request(page, callback=self.parse_page)

            
    def parse_page(self,response):
        print("afghj")
        mydb = MongoDB()
        urls = response.xpath(f'{self.news_xpath}').extract()
        print(urls)
        for url in urls:
            print(url)
            url = self.source_url+url
            is_present = mydb.query(collection_name="articles",search={'url':url})
            if len(is_present) == 0:
                yield scrapy.Request(url,callback=self.parse_news_articles)
            else:
                break
    def parse_news_articles(self, response):
        print("parse_news_articles")
        url = response.url
        description = response.xpath(f'{self.description_xpath}').extract()
        for t_xpath in self.title_xpath:
            try:
                title = response.xpath(f'{t_xpath}').get()
            except:
                pass
            if title != None:
                break

        for img_xpath in self.image_xpath:
            try:
                image = response.xpath(f'{img_xpath}/@src').extract()
            except:
                pass
            if len(image) > 0:
                image = image[0]
                break
        if isinstance(description, list):
            description = "".join(description)
        data = [{
            'source_id': self.source_id,
            'url' : url,
            'title' : title,
            'description' : description,
            'image' : image,
            'topic' : self.topic,
            'language': self.language,
            'is_summarized':0,
            'is_translated': 0,
            'time': self.time
        }]
        if data[0]['title']!= None and len(data[0]['description'])>100 and data[0]['image']!= []:
            self.save(data)
                   
    def save(self,summarized_news):
        print("Saving the records")
        mydb = MongoDB()
        object_id = mydb.insert_many("articles",summarized_news)   
        print(object_id)   