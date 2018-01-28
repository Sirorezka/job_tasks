Project was build on python 3.6 under Windows 10.

**Description**
Search for google trends in CNN news feed. Program parse google trends and parse and store CNN news in ElasticSearch database. For each google trend you can see most relevant CNN article in database. Project has simple web interface that shows result of search queries.

**How it looks**
See screenshot *progr_screenshot.PNG*


**Launch** 

Launch project from docker:

```
# create the network
docker network create cnn_netw

# start the ES container
docker run -d --net cnn_netw -p 9200:9200 -p 9300:9300 --name es elasticsearch

# start the flask app container
docker run -d --net cnn_netw -p 5000:5000 --name cnn_web sirorezka/cnn_news
```

Alternatively you can try to run .sh file:
```
sh run_all.sh
```


**File structure**

*cnn_elastic.py*  - contains parameters for ElasticSearch engine. 
Also it contains class that connects to ES, add new articles and search for query in database

*cnn_news_rss.py* - class that reads and parses cnn news feed. Also it contains function that uploads articles to ElasticSearch database. Class stores news that were loaded on previous iteration to prevent from loading in database news that were already uploaded.

*cnn_flask.py* - Create flask app. Every 30 seconds check for pytrends and new news in CNN RSS feed. Time update parameters can be found here in scheduler function. To update webpage script uses socketio library

*templates/index.html* - page updated using javascript socketio function




 