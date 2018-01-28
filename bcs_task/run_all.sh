# build the flask container
# docker build -t sirorezka/cnn_news .

## finish previous task
docker stop es
docker rm es
docker stop cnn_web
docker rm cnn_web
docker network rm cnn_netw

# create the network
docker network create cnn_netw

# start the ES container
docker run -d --net cnn_netw -p 9200:9200 -p 9300:9300 --name es elasticsearch


# start the flask app container
docker pull sirorezka/cnn_news
echo "sleep for 10 seconds"
sleep 10
ping -n 10 127.0.0.1 >nul
docker run -d --net cnn_netw -p 5000:5000 --name cnn_web sirorezka/cnn_news