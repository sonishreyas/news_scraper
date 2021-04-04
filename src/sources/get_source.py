import os

from src.sources.sources import *
from src.exceptions import source_not_found

class NewsSource:
    def __init__(self,source_id):
        self.id = int(source_id)
        self.information = self.fetch_news_source_data()

    def fetch_news_source_data(self):
        for news_source_info in news_websites:
            if self.id:
                if news_source_info["_id"] == self.id:
                    news_info = news_source_info
                    break
            else:
                if self.id:
                    raise source_not_found("Source with id %d not found".format(self.id))
        return news_info 
