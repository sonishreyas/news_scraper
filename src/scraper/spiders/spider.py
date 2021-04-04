import scrapy
from urllib.parse import urljoin
from src.sources.sources import *
import pandas as pd
from src.scraper.items import *
from src.utilities.summarizer import summarize_english_news
from src.utilities.mongo import MongoDB

class NewsSpider(scrapy.Spider):
    name = 'news'

    def __init__(self, source):
        self.url = kwargs.get("url")
        self.topic = kwargs.get("topic")
        self.page_xpath = kwargs.get("page_xpath")
        self.news_xpath = kwargs.get("news_xpath")
        self.articles_xpath = kwargs.get("articles_xpath")
        self.title_xpath = kwargs.get("title_xpath")
        self.description_xpath = kwargs.get("description_xpath")
        self.image_xpath = kwargs.get("image_xpath")
        self.author_xpath = kwargs.get("author_xpath")
        # self.url = 'https://timesofindia.indiatimes.com/news'
        # self.source_url = "https://timesofindia.indiatimes.com"
        # self.news_xpath = "//*[@class='main-content']/div/ul/li/span/a/@href"
        # self.page_xpath = "//*[@class='curpgcss']/li/a/@href"
        # self.title_xpath = "//*[@class='_2NFXP ']/h1"
        # self.description_xpath = "//*[@class='ga-headlines']"
        # self.author_xpath = "//*[@class='_3Mkg- byline']"

    def start_requests(self):
        yield scrapy.Request(url=self.url, callback=self.parse)
    
    def parse(self, response):
        pages = response.xpath(f'{self.page_xpath}').extract()
        for page in pages:
            page = urljoin(self.url,page)
            yield scrapy.Request(url=page, callback=self.parse_page)
            
    def parse_page(self,response):
        urls = response.xpath(f'{self.news_xpath}').extract()
        for url in urls:
            url = urljoin(self.source_url,url)
            yield scrapy.Request(url=url,callback=self.parse_news_articles)
 
    def parse_news_articles(self, response):
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

        