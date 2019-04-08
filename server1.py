from flask import Flask
import post


app = Flask(__name__)

@app.route('/', methods = ['POST'])
def add_task():
	return post.post_task(request.form['task'])

@app.route('/', methods = ['POST'])
def modify_task():
	return put.put_task(request.form['id'], request.form['new_task'])
