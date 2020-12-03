import scrapy
from urllib.parse import urljoin
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
        self.source_url = "https://timesofindia.indiatimes.com"
        self.news_xpath = "//*[@class='main-content']/div/ul/li/span/a/@href"
        self.page_xpath = "//*[@class='curpgcss']/li/a/@href"
        self.title_xpath = "//*[@class='_2NFXP ']/h1"
        self.description_xpath = "//*[@class='ga-headlines']"
        self.author_xpath = "//*[@class='_3Mkg- byline']"

    def start_requests(self):
        yield scrapy.Request(url=self.url, callback=self.parse)
    
    def parse(self, response):
        pages = response.xpath(f'{self.page_xpath}').extract()
        print(pages) 
        for page in pages:
            page = urljoin(self.url,page)
            yield scrapy.Request(url=page, callback=self.parse_page)
            
    def parse_page(self,response):
        urls = response.xpath(f'{self.news_xpath}').extract()
        for url in urls:
            url = urljoin(self.source_url,url)
            yield scrapy.Request(url=url,callback=self.parse_news_articles)
 
    def parse_news_articles(self, response):
        # item = NewsScraperItem()
        url = response.url
        title =  response.xpath(f'{self.title_xpath}').extract()
        description = response.xpath(f'{self.description_xpath}').extract()
        author = response.xpath(f'{self.author_xpath}').extract()
        print("we are here **********+*++++++++++++++++++++++++**************************")
        df = pd.read_csv("/home/ubuntu/BE/news-aggregator/NEWS_SCRAPER/NEWS_SCRAPER/spiders/news.csv")
        da = {
            'url' : url,
            'title' : title,
            'description' : description,
            'author' : author
            }
        da = pd.DataFrame(da)
        df = pd.concat([df,da])
        df.set_index('url',inplace=True)
        df.to_csv("/home/ubuntu/BE/news-aggregator/NEWS_SCRAPER/NEWS_SCRAPER/spiders/news.csv")
        # yield item

        
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
        