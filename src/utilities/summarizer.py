from transformers import pipeline
import pandas as pd

def summarize_english_news(data):
    summarizer = pipeline("summarization")
    news = []
    for i in data:
        news.append(i['description'])
    result = []
    for article in news:
        inshort = summarizer(article, max_length=130, min_length=30, do_sample=False)
        article['summary'] = inshort[0]['summary_text']
        article['is_summarized'] = 1
        result.append(article)
    return result

    
