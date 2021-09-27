import os

from src.sources.sources import *
from src.exceptions import source_not_found
from src.utilities.mongo import MongoDB

class NewsSource:
    def __init__(self,source_id):
        self.id = int(source_id)
    def fetch_news_source_data_db(self):
        for news_source_info in news_websites:
            if self.id:
                if news_source_info["_id"] == self.id:
                    news_info = news_source_info
                    break
            else:
                if self.id:
                    raise source_not_found("Source with id %d not found".format(self.id))
        return news_info 
    # def fetch_news_source_data_db(self):
    #     mydb = MongoDB()
    #     news_info = mydb.query(collection_name="sources",search={'_id':self.id})
    #     return news_info[0]
