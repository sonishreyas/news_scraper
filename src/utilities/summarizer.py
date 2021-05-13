from transformers import pipeline
import pandas as pd

def summarize_english_news(data):
    summarizer = pipeline("summarization")
    news = []
    for i in data:
        news.append(i['description'])
    result = []
    for article in news:
        try:
            if len(article)> 200:
                inshort = summarizer(article, max_length=200000, min_length=60, do_sample=False)
                article['summary'] = inshort[0]['summary_text']
                article['is_summarized'] = 1
                result.append(article)
        except:
            print("Exception in Summarization!!!!")
            pass
    print(result)
    return result

def summarize():
    df = pd.read_csv("/home/ubuntu/BE/news_scraper/src/test2.csv")
    data = list(df['description'])
    print("11111")
    summarizer = pipeline("summarization")
    print("1111122")
    result = []
    for article in data:
        news = {}
        try:
            print("ider bhi aagaya mein")
            if len(article)> 200:
                inshort = summarizer(article, max_length=200000, min_length=60, do_sample=False)
                news['summary'] = inshort[0]['summary_text']
                news['desc'] = article
            
                
                result.append(news)
        except:
            print("Exception in Summarization!!!!")
    da = pd.DataFrame(result)
    da.to_csv("Final.csv")


# summarize()
    
