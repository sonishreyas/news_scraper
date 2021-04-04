from src.sources import *
from scrapy.crawler import CrawlerRunner

def run_spider(spider,source_information):
    def f():
            runner = CrawlerRunner()
            deferred = runner.crawl(spider,source_information = source_information)
            deferred.addBoth(lambda _: reactor.stop())
            reactor.run()

    p = Process(target=f)
    p.start()
    p.join()
