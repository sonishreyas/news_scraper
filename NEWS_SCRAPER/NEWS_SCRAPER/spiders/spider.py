import scrapy
from NEWS_SCRAPER.sources import *
import pandas as pd

class NewsSpider(scrapy.Spider):
    name = 'news'

    def __init__(self, **kwargs):
        self.url = kwargs.get("url")
        self.topic = kwargs.get("topic")
        self.articles_xpath = kwargs.get("articles_xpath")
        self.title_xpath = kwargs.get("title_xpath")
        self.description_xpath = kwargs.get("description_xpath")
        self.image_xpath = kwargs.get("image_xpath")
        self.author_xpath = kwargs.get("author_xpath")
        
    def start_requests(self):
        yield scrapy.Request(url=self.url, callback=self.parse)
    
    def parse(self, response):
        print("In parse method.")
        self.save(response.request.url, response.text)

    def save(self, source_url, xpath_response):
        # mydb = dbConnection()
        # mycursor = mydb.cursor()
        # news_table = news_table       
        # sql = "INSERT INTO " + news_table + " (url, title, description, author, image, topic, source) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        # source_url = urllib.parse.quote(source_url)
        # mycursor.execute(sql, val)
        # mydb.commit()
        # mycursor.close()
        print(source_url)

        