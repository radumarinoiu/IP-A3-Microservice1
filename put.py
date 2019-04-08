import pymongo
import json

from pymongo import MongoClient
client = MongoClient()

db = client['tasks_db']
tasks = db['tasks']

def put_task(task)
	tasks.update_one({'creare': task['creare']}, {'nume': task['nume'], 'expirare': task['expirare']}, upsert = False)
