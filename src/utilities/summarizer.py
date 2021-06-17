from transformers import pipeline
import pandas as pd
import logging
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 

def summarize_english_news(data):
    summarizer = pipeline("summarization")
    result = []
    for article in data:
        try:
            if len(article['description'])> 100:
                inshort = summarizer(article['description'], max_length=len(article['description']), min_length=60, do_sample=False)
                article['summary'] = inshort[0]['summary_text']
                article['is_summarized'] = 1
                result.append(article)
        except:
            print("Exception in Summarization!!!!")
            pass
    # print(result)
    return result

def summarize_news(data):
    summarizer = pipeline("summarization")
    try:
        inshort = summarizer(data['description'], max_length=len(data['description']), min_length=60, do_sample=False)
        data['summary'] = inshort[0]['summary_text']
        data['is_summarized'] = 1
    except:
        print("Exception in Summarization!!!!")
        data['summary'] = ""
        pass
    return data