import scrapy
from NEWS_SCRAPER.sources import *
import pandas as pd
from NEWS_SCRAPER.items import *

class NewsSpider(scrapy.Spider):
    name = 'news'

    def __init__(self, **kwargs):
        # self.url = kwargs.get("url")
        # self.topic = kwargs.get("topic")
        # self.page_xpath = kwargs.get("page_xpath")
        # self.news_xpath = kwargs.get("news_xpath")
        # self.articles_xpath = kwargs.get("articles_xpath")
        # self.title_xpath = kwargs.get("title_xpath")
        # self.description_xpath = kwargs.get("description_xpath")
        # self.image_xpath = kwargs.get("image_xpath")
        # self.author_xpath = kwargs.get("author_xpath")
        self.url = 'https://timesofindia.indiatimes.com/news'
        self.news_xpath = "//*[@class='main-content']/div/ul/li/span/a"
        self.page_xpath = "//*[@id='itemContainer'][2]/li/a"
    def start_requests(self):
        yield scrapy.Request(url=self.url, callback=self.parse)
    
    def parse(self, response):
        print("In parse method.")
        pages = response.xpath(f'{self.page_xpath}/@href').extract()
        print(pages) 
        for page in pages:
            print("here.......................................................................")
            yield scrapy.Request(url=page, callback=self.parse_page)
            
    def parse_page(self,response):
        urls = response.xpath(f'{self.news_xpath}/@href').extract()
        for url in urls:
            print("here.......................................................................:::::::;;",url)
            yield scrapy.Request(url=url,callback=self.parse_news_articles)
 
    def parse_news_articles(self, response):
        item = NewsScraperItem()
        item['url'] = response.url
        item['title'] =  response.xpath(f'{self.title_xpath}/text()').extract()
        item['description'] = response.xpath(f'{self.description_xpath}/text()').extract()
        item['author'] = response.xpath(f'{self.author_xpath}/text()').extract()
        print("we are here **********+*++++++++++++++++++++++++**************************")
        yield item

        
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

# if __name__="__main__":

#     nw = NewsSpider()
        