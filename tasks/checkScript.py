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

with open('object.json') as json_file:
    json_data = json.load(json_file)
    for data in json_data['sub-tasks']:
        isCompleted = 0
        subTask = json.load(db.getById(data['id']))
        if(subTask['status'] == '1'):
            isCompleted = 1
        else:
            isCompleted = 0
            break
    if(isCompleted == 1):
        json_data['status'] = '1'
