from flask import Flask, request, render_template, flash
import json
import pandas as pd
import os
from elasticsearch import Elasticsearch, helpers
import time
import random

#PROMETHEUS MONITORING
from prometheus_client import start_http_server
from prometheus_client import Counter
from prometheus_client import Gauge
from prometheus_client import Summary
from prometheus_client import Histogram
#END PROMETHEUS MONITORING

#PROMETHEUS MONITORING
REQUESTS = Counter('twitter_flask_app_requests_total','How many times the Twitter application has been accessed ?')
EXCEPTIONS = Counter('twitter_flask_app_exceptions_total','How many times the Twitter application issued an exception ?')
SEARCH = Counter('twitter_flask_app_nb_search','How many search in the Twitter application have been made ?')

INPROGRESS = Gauge('twitter_flask_app_inprogress_gauge','How many requests to the Twitter application are currently in progress ?')
LAST = Gauge('twitter_flask_app_last_accessed_gauge','When was the Twitter application last accessed ?')

LATENCY = Summary('twitter_flask_app_latency','Time needed for a request ?')

#LATENCY_HIS = Histogram('twitter_flask_app_latency_hist','Time needed for a request ?')
LATENCY_HIS = Histogram('twitter_flask_app_latency_hist','Time needed for a request ?', buckets=[0.0001,0.001,0.01,0.1,1.0,1.5,2.0,3.0])
#END PROMETHEUS MONITORING

app = Flask(__name__)
app.secret_key = 'my_secret_key'

#return the best match
def submit_txt(es, index, txt):
	query=es.search(index=index,
		 body={
	 "query": {
	     "match": {
		 "text.english": {
		     "query": txt,
		     }
		 }
	     },
	 "size": 20
	    }
	)
	#send the best similar tweets to the web api
	for el in query['hits']['hits']:
            flash(el['_id'])
            flash(el['_source']['text'])
            flash(el['_score'])
	#PROMETHEUS MONITORING
	#INPROGRESS.dec()
	SEARCH.inc()
	#END PROMETHEUS MONITORING
	return render_template('interface.html')

def create_index(es, index, mapping):
	print("Creating index...\n")
	response = es.indices.create(
	    index=index,
	    body=mapping,
	    ignore=400)
	if 'acknowledged' in response:
		if response['acknowledged'] == True:
			print ("INDEX MAPPING SUCCESS FOR INDEX:", response['index'])

	#PROMETHEUS MONITORING
	#INPROGRESS.dec()
	#END PROMETHEUS MONITORING
	return index

def ingest_data(es, index, data):
	print("Ingesting data to ES...\n")
	all_tweets=({'_id': doc['id'],'text': doc['text'], '_index': index } for doc in data)
	helpers.bulk(es,all_tweets)
	print("Data loaded into ES.\n")

@app.route('/', methods=['GET', 'POST'])
def index():
	#PROMETHEUS MONITORING
	REQUESTS.inc()
	with EXCEPTIONS.count_exceptions():
		if random.random() < 0.2 :
			raise Exception

	INPROGRESS.inc()
	LAST.set(time.time())
	start = time.time()
	time.sleep(5)

	#END PROMETHEUS MONITORING
	if request.method == 'POST':
		details = request.form
		if details['form_type'] == 'submit_txt':
			return submit_txt(es, index, details['txt'])

	#PROMETHEUS MONITORING
	INPROGRESS.dec()
	lat = time.time()
	LATENCY.observe(lat - start)
	LATENCY_HIS.observe(lat - start)
	#END PROMETHEUS MONITORING
	return render_template('interface.html')



if __name__ == '__main__':

	#PROMETHEUS MONITORING
	print("Lauching the metrics of the application...\n")
	start_http_server(8010)
	#END PROMETHEUS MONITORING
	print("Lauching the web interface...\n")
	print("Connecting to Elastic...\n")
	es = Elasticsearch(['http://elasticsearch:9200/'], verify_certs=True)
	while not es.ping():
		time.sleep(5)

	print("Connected to Elastic\n")
	print("Retrieving data from CSV...\n")
	#retrieving the csv keep only 2columns
	df= pd.read_csv('tweets.csv')
	df=df[['id','text']]
	df.to_json('tweets.json',orient='records')


	#load the json file
	with open('tweets.json') as file:
	    data=file.read()
	data=json.loads(data)

	#load the mapping
	with open('mapping.json') as file:
	    mapping=file.read()
	mapping=json.loads(mapping)

	index = create_index(es, 'tweets_trump', mapping)
	ingest_data(es, index, data)
	time.sleep(5)
	app.run(host='0.0.0.0')
