import argparse
from src.sources.get_source import NewsSource
from src.exceptions import *
from src.scraper.spiders.spider import NewsSpider
from src.utilities.utilities import run_spider
from src.utilities.summarizer import summarize_news
from src.utilities.mongo import MongoDB
from src.utilities.translate import translate
from src.sources.languages import languages

def scrape_news(source):
    print("asdas")
    run_spider(NewsSpider,source_information=source)

def summarize(id):
        print("in summarizer")
        mydb = MongoDB()
        results = mydb.query(collection_name="articles",search={'is_summarized':0,'source_id':id})
        summarized_news = {}
        for data in results:
            if data['language'] == "english":
                summarized_news = summarize_news(data)
                mydb.find_and_update(collection_name="articles",search={'_id': data['_id']},new_fields={'is_summarized':summarized_news['is_summarized'],'summary': summarized_news['summary'],'original_summary': summarized_news['original_summary']})
        mydb.close_connection()

def translate_summary(id):
    print("In translators")
    mydb = MongoDB()
    results = mydb.query(collection_name="articles",search={'is_translated':0,'source_id':id,'is_summarized':1})
    for article in results:
        a = {'is_translated':1}
        for lang in languages:
            title = translate(lang['ISO-639-1 Code'],article['title'])
            summary = translate(lang['ISO-639-1 Code'],article['summary'])
            a[f'{lang["Language"]}_summary'] = summary
            a[f'{lang["Language"]}_title'] = title
        mydb.find_and_update(collection_name="articles",search={'_id':article['_id']},new_fields=a)
    mydb.close_connection()

def run_scripts(source, script_id):
    if script_id == 1:
        print("Running 1st script")
        scrape_news(source)
    elif script_id == 2:
        print("Running 2nd script")
        summarize(source['_id'])
    elif script_id == 3:
        print("Running 3rd script")
        translate_summary(source['_id'])
    
if  __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-id","--source_id",required=True, help="Provide the Source Id")
    parser.add_argument("-script_id","--script_id",required=True, help="Provide the Script Id to run")
    args = parser.parse_args()
    if not args.source_id:
        raise missing_source_id_argument("Argument --source_id is mandatory")
    source = NewsSource(args.source_id)
    source_information = source.fetch_news_source_data_db()
    if not args.script_id:
        script_ids = [1,2,3]
    elif "," not in args.script_id:
        script_ids = [args.script_id]
    else:
        script_ids = args.script_id.split(",")
    for i in script_ids:
        run_scripts(source_information,int(i))
