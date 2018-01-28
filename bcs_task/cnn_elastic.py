
## https://www.elastic.co/guide/en/elasticsearch/client/python-api/current/index.html
##  http://elasticsearch-py.readthedocs.io/en/master/api.html
##  https://habrahabr.ru/post/280488/


from datetime import datetime
from elasticsearch import Elasticsearch, client

## params for elastisearch database
##
ANALYZER_PARAMS = {
  "settings": {
    "analysis": {
     "filter" : {"eng_stemmer" : {"type" : "stemmer","language" : "english"},
                 "english_stop":{"type":"stop","stopwords":"_english_"}
                 },
      "analyzer": {
        "default": {
          "type":"custom",
          "char_filter": ["html_strip"],
          "tokenizer": "standard",
          "filter": [
            "lowercase",
            "english_stop",
            "eng_stemmer"
          ]
        }
      }
    }
  },
  "mappings": {
    "article": {
    "properties": {
            "published": {"type": "date"},
            "title": {"type": "text","fielddata": True},
            "summary": {"type": "text"},
            "title_summary": {"type": "text"}
      }}}
}


class cnn_es_engine():
	def __init__(self, delete_index=True):

		self.es = Elasticsearch()
		if delete_index:
			self.es.indices.delete(index='cnn_news', ignore=[400, 404])
			es_analyzer = client.IndicesClient(self.es)
			es_analyzer.create(index='cnn_news',body = ANALYZER_PARAMS)

	## add cnn article to database
	def add_article(self,doc,verbose = False):
		res = self.es.index(index="cnn_news", doc_type='article', body=doc)
		self.es.indices.refresh(index="cnn_news")
		if verbose:
			print(res['result'])

	## make query search
	def search_query(self, val_query, val_size = 1):
		query_body = {"query": {"bool": {
				'must': [{'match':{'title_summary':val_query}}] 
				}}}
		res = self.es.search(index="cnn_news", body=query_body,
				size = val_size)
		return res


if __name__ == "__main__":
	doc = {
		'published': datetime.now(),
	    'title': 'Sanctions on N. Korea are strangling Chinese city',
	    'summary': '<img src="http://feeds.feedburner.com/~r/rss/edition_world/~4/_R0OefDg5Kc" height="1" width="1" alt=""/>',
	    'title_summary': 'Sanctions on N. Korea are strangling Chinese city <img src="http://feeds.feedburner.com/~r/rss/edition_world/~4/_R0OefDg5Kc" height="1" width="1" alt=""/>'
	}


	cnn_es = cnn_es_engine()
	cnn_es.add_article(doc,verbose=True)
	cnn_es.add_article(doc,verbose=True)
	cnn_es.add_article(doc,verbose=True)
	cnn_es.search_query("china korea",val_size=3)
