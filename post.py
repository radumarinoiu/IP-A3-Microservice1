import pymongo
import datetime
import json
from pymongo import MongoClient

client = MongoClient()
db = client['tasks_db']

def post_task(task)

	post = {nume: task["nume"], creare: task["creare"], expirare: task["expirare"]}
	posts = db.tasks
	post_id = posts.insert_one(post).inserted_id
