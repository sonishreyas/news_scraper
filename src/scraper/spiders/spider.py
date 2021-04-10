import scrapy
from urllib.parse import urljoin
from src.sources.sources import *
import pandas as pd
from src.scraper.items import *
from src.utilities.summarizer import summarize_english_news
from src.utilities.mongo import MongoDB

class NewsSpider(scrapy.Spider):
    name = 'news'

    def __init__(self, source_information):
        self.url = source_information.get("url")
        self.topic = source_information.get("topic")
        self.page_xpath = source_information.get("page_xpath")
        self.news_xpath = source_information.get("news_xpath")
        self.articles_xpath = source_information.get("articles_xpath")
        self.title_xpath = source_information.get("title_xpath")
        self.description_xpath = source_information.get("description_xpath")
        self.image_xpath = source_information.get("image_xpath")
        self.author_xpath = source_information.get("author_xpath")


    def start_requests(self):
        yield scrapy.Request(url=self.url, callback=self.parse)
    
    def parse(self, response):
        print("In parse request")

        pages = response.xpath(f'{self.page_xpath}').extract()
        print(pages)
        for page in pages:
            page = urljoin(self.url,page)
            yield scrapy.Request(url=page, callback=self.parse_page)
            
    def parse_page(self,response):
        print("In parse page request")

        urls = response.xpath(f'{self.news_xpath}').extract()
        print(urls)
        for url in urls:
            url = urljoin(self.source_url,url)
            yield scrapy.Request(url=url,callback=self.parse_news_articles)
 
    def parse_news_articles(self, response):
        print("inside parse_news_articles")
        url = response.url
        title =  response.xpath(f'{self.title_xpath}').get()
        description = response.xpath(f'{self.description_xpath}').get()
        author = response.xpath(f'{self.author_xpath}').extract()
        print("we are here **********+*++++++++++++++++++++++++**************************")
        data = [{
            'url' : url,
            'title' : title,
            'description' : description,
            'author' : author
        }]
        summarized_news = summarize_english_news(data)
        self.save(summarized_news)
        
    def save(self,summarized_news):
        mydb = MongoDB()
        object_id = mydb.insert_many(news,summarized_news)

        