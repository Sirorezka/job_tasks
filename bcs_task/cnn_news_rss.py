import feedparser
import pandas as pd

import re

from datetime import datetime


###  Read and preprocess news rss feed
###

class rss_news_reader:

    ## definition is straightforward
    ## new_flag - is True if article is new in search
    ##
    def __init__(self, news_link):
        self.news_link  = news_link
        self.rss_news = feedparser.parse(self.news_link)
        self.news = pd.DataFrame([["","","","","",""]])
        self.news.columns = ['published','title','link','summary','title_summary',"new_flag"]

    ## if "only_new" then feed reader will select only the news that weren't saved before
    def read_news_feed(self):
        all_news = []

        for news_entry in self.rss_news['entries']:
            news_title = news_entry['title']
            news_title = re.sub('<[^<]+?>', '', news_title)

            news_link = news_entry['link']
            try:
                news_summary = news_entry['summary']
                news_summary = re.sub('<[^<]+?>', '', news_summary)
            except:
                news_summary = ""
            try:
                news_published = news_entry['published']
                ## print  (news_published)
                news_published = datetime.strptime(news_published, '%a, %d %b %Y %H:%M:%S %Z')
            except:
                news_published =  datetime.now()
            
            news_title_text =  news_title + " " + news_summary
            new_flag = False ## tag if news is new
            news_arr = [news_published,news_title,news_link,news_summary,news_title_text,new_flag]
            all_news.append(news_arr)

        all_news = pd.DataFrame(all_news)
        col_names = ['published','title','link','summary','title_summary','new_flag']
        all_news.columns = col_names
        ## print (all_news.head())

        ## check if article is new in feed
        all_news = all_news.merge(self.news,how='left',on='title_summary',suffixes=("","_y"))
        all_news['new_flag'] = pd.isnull(all_news['published_y'])  ## flag all new articles
        all_news = all_news[col_names].copy(deep=True)

        self.news = all_news
		
    def upload_news_to_es(self,cnn_es):
        new_articles = self.news.query('new_flag==True').drop('new_flag',axis=1).to_dict('records')
        for article in new_articles:
            cnn_es.add_article(article)
        print ("articles uploaded to es: ",len(new_articles))
    
if __name__ == "__main__":
    cnn_link = 'http://rss.cnn.com/rss/edition_world.rss'
    cnn_rss = rss_news_reader(cnn_link)
    cnn_rss.read_news_feed()
    print (cnn_rss.news.head())