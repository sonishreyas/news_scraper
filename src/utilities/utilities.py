from src.sources import *
from scrapy.crawler import CrawlerRunner
from multiprocessing import Process
from twisted.internet import reactor

def run_spider(spider,source_information):
    def f():
            runner = CrawlerRunner()
            deferred = runner.crawl(spider,source_information = source_information)
            deferred.addBoth(lambda _: reactor.stop())
            reactor.run()

    p = Process(target=f)
    p.start()
    p.join()
