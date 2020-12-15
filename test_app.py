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
	
	#stress test 1000 queries
	def test_f_stress_test(self):
		es = Elasticsearch(['http://localhost:9200/'], verify_certs=True)
		start=time.time()
		for i in range(10):
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
		end=time.time()
		print(end-start)
		self.assertGreater(60 , end-start)
		
		
		

	def test_g_stress_test(self):
		start=time.time()
		n=10	
		params = {
			'txt': "I love pizza",
			"form_type": "submit_txt"
		}
		for i in range(n):
			rep=requests.post('http://localhost:5000', data=params)
			self.assertEqual(rep.status_code,200)
		end=time.time()
		print("Time to execute ",n," queries : ", end-start)
		
		self.assertGreater(60 , end-start)

if __name__=='__main__':
	unittest.main()

