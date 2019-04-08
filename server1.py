from flask import Flask
import post
import requests
import put


app = Flask(__name__)

@app.route('/', methods = ['POST'])
def add_task():
	return post.post_task(request.get_json())

@app.route('/', methods = ['POST'])
def modify_task():
	return put.put_task(request.get_json())
