import feedparser
import pandas as pd

class rss_news_reader:
    def __init__(self, news_link):
        self.news_link  = news_link
        self.rss_news = feedparser.parse(self.news_link)
        self.news = pd.DataFrame()
        
    def read_news_feed(self):
        all_news = []

        for news_entry in self.rss_news['entries']:
            news_title = news_entry['title']
            news_link = news_entry['link']
            try:
                news_summary = news_entry['summary']
            except:
                news_summary = ""
            news_arr = [news_title,news_link,news_summary]
            all_news.append(news_arr)

        all_news = pd.DataFrame(all_news)
        all_news.columns = ['title','link','summary']
        self.news = all_news
