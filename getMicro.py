import pymongo

from pymongo import MongoClient
from bson.objectid import ObjectId


client = MongoClient('vvtsoft.ddns.net', '5120')

db = client['db']

tasks = db.tasks

task_cursor = tasks.find( {"_id" : ObjectId("5ca3d06afc79d3e5d41fc0de") } )

list(task_cursor)