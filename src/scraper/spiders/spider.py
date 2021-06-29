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

class NewsSpider(scrapy.Spider):
    name = 'news'

    def __init__(self, source_information):
        self.source_id = source_information.get("_id")
        self.url = source_information.get("url")
        self.topic = source_information.get("topic")
        self.source_url = source_information.get("source_url")
        self.page_xpath = source_information.get("page_xpath")
        self.news_xpath = source_information.get("news_xpath")
        self.articles_xpath = source_information.get("articles_xpath")
        self.title_xpath = source_information.get("title_xpath")
        self.description_xpath = source_information.get("description_xpath")
        self.image_xpath = source_information.get("image_xpath")
        self.author_xpath = source_information.get("author_xpath")
        self.language = source_information.get("language")
        self.time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    def start_requests(self):
        yield scrapy.Request(url=self.url, callback=self.parse)
        
    def parse(self, response):
        pages = response.xpath(self.page_xpath).extract()
        for page in pages:
            page = urljoin(self.url,page)
            yield scrapy.Request(url=page, callback=self.parse_page)
            
    def parse_page(self,response):
        mydb = MongoDB()
        urls = response.xpath(f'{self.news_xpath}').extract()
        for url in urls:
            url = self.source_url+url
            is_present = mydb.query(collection_name="articles",search={'url':url})
            if len(is_present) == 0:
                yield scrapy.Request(url=url,callback=self.parse_news_articles)
            else:
                break
    def parse_news_articles(self, response):
        url = response.url
        title =  response.xpath(f'{self.title_xpath}').get()
        description = response.xpath(f'{self.description_xpath}').extract()
        author = response.xpath(f'{self.author_xpath}').extract()
        image = response.xpath(f'{self.image_xpath}/@src').extract()[0]
        if isinstance(description, list):
            description = "".join(description)
        data = [{
            'source_id': self.source_id,
            'url' : url,
            'title' : title,
            'description' : description,
            'author' : author,
            'image' : image,
            'topic' : self.topic,
            'language': self.language,
            'is_summarized':0,
            'is_translated': 0,
            'time': self.time
        }]
        if data[0]['title']!= None and len(data[0]['description'])>100:
            self.save(data)
        
        # self.summarize(data)

    # def summarize(self,data):
    #     print("in summarizer")
    #     mydb = MongoDB()
    #     if data[0]["description"] != "":
    #         if self.language == "english":
    #             summarized_news = summarize_english_news(data)
    #             self.languages(summarized_news)

    # def languages(self,summarized_news):
    #     print("In translators")
    #     result = []
    #     for article in summarized_news:
    #         a = article
    #         for lang in languages:
    #             title = translate(lang['ISO-639-1 Code'],article['title'])
    #             summary = translate(lang['ISO-639-1 Code'],article['summary'])
    #             a[f'{lang["Language"]}_summary'] = summary
    #             a[f'{lang["Language"]}_title'] = title
    #         result.append(a)
    #     self.save(result)
                   
    def save(self,summarized_news):
        print("Saving the records")
        mydb = MongoDB()
        object_id = mydb.insert_many("articles",summarized_news)   
        print(object_id)   