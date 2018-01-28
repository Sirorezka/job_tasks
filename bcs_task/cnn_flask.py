from flask import Flask, render_template
from apscheduler.schedulers.background import BackgroundScheduler
from flask_socketio import SocketIO, emit

## https://flask-socketio.readthedocs.io/en/latest/
## https://stackoverflow.com/questions/18395976/how-to-display-a-json-array-in-table-format

##
## https://flask-socketio.readthedocs.io/en/latest/

from pytrends.request import TrendReq
from random import random
import pandas as pd
import time
from cnn_elastic import *
from cnn_news_rss import *


app = Flask(__name__)
socketio = SocketIO(app)
cnn_es = cnn_es_engine()
news_reader = rss_news_reader('http://rss.cnn.com/rss/edition_world.rss')
news_reader.read_news_feed()
news_reader.upload_news_to_es(cnn_es)

news_reader2 = rss_news_reader('http://rss.cnn.com/rss/edition.rss')
news_reader2.read_news_feed()
news_reader2.upload_news_to_es(cnn_es)

## print (news_reader.news.head())  


## read google trend searches
## look up for trends in news database
def gg_trend_search(cnn_es = cnn_es):
    gg_trends = TrendReq(hl='en-US', tz=360)
    tt = gg_trends.trending_searches()
    tt['title']

    search_res = []

    for trend_val in tt['title']:
        ##print (trend_val)
        trend_val_mod = re.sub("2018","",trend_val)
        es_cnn_res = cnn_es.search_query(trend_val_mod,val_size=1)
        try:
            score_val = es_cnn_res['hits']['hits'][0]['_score']
            article_val = es_cnn_res['hits']['hits'][0]['_source']['title_summary']
            link_val = es_cnn_res['hits']['hits'][0]['_source']['link']
            publish_val = es_cnn_res['hits']['hits'][0]['_source']['published']

        except:
            score_val = 0
            article_val = "None"
            link_val = "None"
            publish_val = None
        search_res.append([trend_val,score_val,article_val,link_val,publish_val])
        
    search_res = pd.DataFrame(search_res)
    search_res.columns = ['trend','score','article','link','published']
    return search_res

## Main job that searches for google trends in current news database
## 
def job(news_reader = news_reader):
    gg_search_db = gg_trend_search()
    socketio.emit('cnn news update',gg_search_db.transpose().to_json(), broadcast=True)

def cnn_read_feed(cnn_es = cnn_es):
    news_reader.read_news_feed()
    news_reader.upload_news_to_es(cnn_es)

    news_reader2.read_news_feed()
    news_reader2.upload_news_to_es(cnn_es)

    print ("job read rss done")

	
#schedule job
scheduler = BackgroundScheduler()
running_job1 = scheduler.add_job(cnn_read_feed, 'interval', seconds=30, max_instances=1)
running_job2 = scheduler.add_job(job, 'interval', seconds=30, max_instances=1)
running_job3 = scheduler.add_job(job)

scheduler.start()

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__': 
    socketio.run(app, host='0.0.0.0')  
    job()
