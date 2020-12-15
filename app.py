from flask import Flask, request, render_template, flash
import json
import pandas as pd
import os
from elasticsearch import Elasticsearch, helpers
import time

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
	return index

def ingest_data(es, index, data):
	print("Ingesting data to ES...\n")
	all_tweets=({'_id': doc['id'],'text': doc['text'], '_index': index } for doc in data)
	helpers.bulk(es,all_tweets)
	print("Data loaded into ES.\n")

@app.route('/', methods=['GET', 'POST'])
def index():
	if request.method == 'POST':
		details = request.form	
		if details['form_type'] == 'submit_txt':
			return submit_txt(es, index, details['txt'])
	return render_template('interface.html')



if __name__ == '__main__':
	print("Lauching the wep interface...\n")
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
	
	
	
	
	
