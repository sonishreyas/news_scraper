from transformers import pipeline
import pandas as pd
def summarize_english_news():
    summarizer = pipeline("summarization")
    df = pd.read_csv('/home/ubuntu/BE/news-aggregator/NEWS_SCRAPER/NEWS_SCRAPER/spiders/news.csv')
    # df = df[df['is_summarized'] == 0]
    news = list(df['description'])
    sa = []
    for article in news:
        inshort = summarizer(article, max_length=130, min_length=30, do_sample=False)
        sa.append(inshort[0]['summary_text'])
    df['summary'] = sa
    df['is_summarized'] = 1
    df.to_csv('/home/ubuntu/BE/news-aggregator/NEWS_SCRAPER/NEWS_SCRAPER/spiders/news.csv')

summarize_english_news()