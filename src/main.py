import argparse
from src.sources.get_source import NewsSource
from src.exceptions import *
from src.scraper.spiders.spider import NewsSpider
from src.utilities.utilities import run_spider

def scrape_news(source):
    run_spider(source_information=source)

if  __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-id","--source_id",required=True, help="Provide the Source Id")
    args = parser.parse_args()
    if not args.source_id:
        raise missing_source_id_argument("Argument --source_id is mandatory")

    source = NewsSource(args.source_id)
    scrape_news(source)