Project was build on python 3.6 under Windows 10.

Launch project from docker:

```
# create the network
docker network create cnn_netw

# start the ES container
docker run -d --net cnn_netw -p 9200:9200 -p 9300:9300 --name es elasticsearch

# start the flask app container
docker run -d --net cnn_netw -p 5000:5000 --name cnn_web sirorezka/cnn_news
```


File structure:

*cnn_elastic.py*  - contains parameters for ElasticSearch engine. 
Also it contains class that connects to ES, add new articles and search for query in database

*cnn_news_rss.py* - class that reads and parses cnn news feed. Also it contains function that uploads articles to ElasticSearch database. Class stores news that were loaded on previous iteration to prevent from loading in database news that were already uploaded.

*cnn_flask.py* - Create flask app. Every 30 seconds check for pytrends and new news in CNN RSS feed. Time update parameters can be found here in scheduler function. To update webpage script uses socketio library

*templates/index.html* - page updated using javascript socketio function




 