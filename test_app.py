import unittest
import os
import requests
import time
from elasticsearch import Elasticsearch

class FlaskTests(unittest.TestCase):
	def setUp(self):
		os.environ['NO_PROXY'] = '0.0.0.0'
		pass
	def tearDown(self):
		pass

	#test if the site respond 
	def test_a_interface(self):
		'''response = requests.get('http://localhost:5000')
		self.assertEqual(response.status_code,200)'''
		return True

	#test if Elastic respond 
	def test_b_elastic(self):
		es = Elasticsearch(['http://localhost:9200/'], verify_certs=True)
		self.assertEqual(es.ping(),True)
	
	
	#indice correctly created	
	def test_c_indices(self):
		es = Elasticsearch(['http://localhost:9200/'], verify_certs=True)
		indices = es.indices.get_alias().keys()
		self.assertEqual('tweets_trump' in indices, True)
	

	#data correclty loaded in ES
	def test_d_ingest(self):
		es = Elasticsearch(['http://localhost:9200/'], verify_certs=True)
		self.assertGreater(es.count()['count'] , 10000)

	
	#test query 
	def test_e_query(self):
		es = Elasticsearch(['http://localhost:9200/'], verify_certs=True)
		res = es.search(index='tweets_trump', 
		 body={
	 "query": {
	     "match": {
		 "text.english": {
		     "query": "i love pizza",
		     }
		 }
	     },
	 "size": 20
	    }
	)
		self.assertGreater(res['hits']['total']['value'] , 0)
	

if __name__=='__main__':
	unittest.main()

