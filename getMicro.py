import pymongo

from pymongo import MongoClient
from bson.objectid import ObjectId


client = MongoClient('vvtsoft.ddns.net', 5120)

db = client['db']

tasks = db.tasks

getAll_cursor = tasks.find( {}, {'name' : 1, '_id' : 0} )

list(getAll_cursor)
