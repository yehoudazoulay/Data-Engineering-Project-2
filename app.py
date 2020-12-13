from flask import Flask, request, render_template, flash
import json
import pandas as pd
import os

app = Flask(__name__)
app.secret_key = 'my_secret_key'


@app.route('/', methods=['GET', 'POST'])
def index():
	if request.method == 'POST':
		details = request.form	
		if details['form_type'] == 'submit_txt':
			return submit_txt(es, index, details['txt'])
	return render_template('interface.html')



if __name__ == '__main__':
	#retrieving the csv keep only 2columns
	df= pd.read_csv('tweets.csv')
	df=df[['id','text']]
	df.to_json('tweets.json',orient='records')


	#load the json file
	with open('tweets.json') as file:
	    data=file.read()
	data=json.loads(data)
	
	app.run(host='0.0.0.0')
	
	
	
	
	
