# build the flask container
# docker build -t sirorezka/cnn_news .

# create the network
docker network create cnn_netw

# start the ES container
docker run -d --net cnn_netw -p 9200:9200 -p 9300:9300 --name es elasticsearch


# start the flask app container
docker pull sirorezka/cnn_news
docker run -d --net cnn_netw -p 5000:5000 --name cnn_web sirorezka/cnn_news