import db

import json
import pymongo
import logging
import traceback

from pymongo import MongoClient
from bson.objectid import ObjectId
from bson.errors import InvalidId as InvalidIdException
from flask import jsonify
from jsonschema import validate

isCompleted = 0

json_data = json.load(db.getById('5cd8130110ecd110d6d61f15'))
for data in json_data[0]['sub-tasks']:
    subTask = json.load(db.getById(data['_id']))
    if(subTask['status'] == '1'):
        isCompleted = 1
    else:
        isCompleted = 0
        break
if(isCompleted == 1):
    json_data['status'] = '1'
    print "Completed"
else:
    print "Not Completed"
