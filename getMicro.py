import pymongo

from pymongo import MongoClient
from bson.objectid import ObjectId


db_username = "devs"
db_password = "devs"

client = MongoClient("mongodb://{}:{}@localhost/tasks_db".format(db_username, db_password))
tasks_db = client["tasks_db"]
tasks = tasks_db["tasks"]

getAll_cursor = tasks.find({}, {"name" : 1, "_id" : 0})

print(list(getAll_cursor))
