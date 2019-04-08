import pymongo
import datetime
import json
from pymongo import MongoClient


db_username = "devs"
db_password = "devs"

client = MongoClient("mongodb://{}:{}@localhost/tasks_db".format(db_username, db_password)

tasks_db = client['tasks_db']
tasks = tasks_db["tasks"]

def post_task(task)

	post = {'nume': task["nume"], 'creare': task["creare"], 'expirare': task["expirare"]}
	posts = tasks
	post_id = posts.insert_one(post).inserted_id
	return post_id

def put_task(task)
	tasks.update_one({'creare': task['creare']}, {'nume': task['nume'], 'expirare': task['expirare']}, upsert = False)
	
