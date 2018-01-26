import feedparser
import pandas as pd

import feedparser
import pandas as pd

from datetime import datetime

class rss_news_reader:
    def __init__(self, news_link):
        self.news_link  = news_link
        self.rss_news = feedparser.parse(self.news_link)
        self.news = pd.DataFrame([["","","","",""]])
        self.news.columns = ['published','title','link','summary','title_summary']

    ## if "only_new" then feed reader will select only the news that weren't saved before
    def read_news_feed(self, only_new=True):
        all_news = []

        for news_entry in self.rss_news['entries']:
            news_title = news_entry['title']
            news_link = news_entry['link']
            try:
                news_summary = news_entry['summary']
            except:
                news_summary = ""
            try:
                news_published = news_entry['published']
                ## print  (news_published)
                news_published = datetime.strptime(news_published, '%a, %d %b %Y %H:%M:%S %Z')
            except:
                news_published = None
            
            news_title_text =  news_title + " " + news_summary
            news_arr = [news_published,news_title,news_link,news_summary,news_title_text]
            all_news.append(news_arr)

        all_news = pd.DataFrame(all_news)
        col_names = ['published','title','link','summary','title_summary']
        all_news.columns = col_names
        if only_new:
             all_news = all_news.merge(self.news,how='left',on='title_summary',suffixes=("","_y")).query("summary_y != summary_y").copy(deep=True)
             all_news = all_news[col_names]
        self.news = all_news
		
