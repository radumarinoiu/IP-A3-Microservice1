import pymongo
import json

from pymongo import MongoClient
from bson.objectid import ObjectId
from flask import jsonify
from flask import Response
from flask import make_response

db_username = "devs"
db_password = "devs"

client = MongoClient("mongodb://{}:{}@localhost/tasks_db".format(db_username, db_password))
db = client["tasks_db"]
coll = db["tasks"]

def getAll():
    getAllList = list(coll.find({}))
    for task in getAllList:
        task["_id"] = str(task["_id"])
    return jsonify(getAllList)

def getById(id):
    getByIdElem = coll.find_one({"_id" : ObjectId(id)})
    if not getByIdElem:
        return make_response(jsonify(""), 404)
    else:
        getByIdElem["_id"] = str(getByIdElem["_id"])
        return jsonify(getByIdElem)

def check_deadline(deadline):
    if deadline["date"] is "null" or deadline["time"] is "null":
        return False
    return True
    


def check_participants(participant):
    if participant["id"] is "null":
        return "participant has not id set"
    if participant["name"] is "null":
        return "participant name has not been set"
    if participant["thumbnail"] is "null":
        return "participant thumbnail is not set"
    if participant["role"] is "null":
        return "participant role is not set"


def post_task(task):
    if task["id"] is "null":
        return "asd"
    if task["name"] is "null":
        return "name not found"
    if task["category"] is "null":
        return "category not found"
    if task["department"] is "null":
        return "department not found"
    if check_deadline(task["deadline"]) is False:
        return "deadline is not set"
    if task["creator"] is "null":
        return "deadline not found"
    if task["description"] is "null":
        return "description is not set"
    if task["priority"] is "null":
        return "priority is not set"
    if task["status"] is "null":
        return "status is not set"
    for part in task["participants"]:
        if check_participants(part) is False:
            return "participant is not set"
    for sub_task in task["sub-tasks"]:
        if sub_task["subtask-id"] is "null":
            return "subtask id is not set"
        if sub_task["deadline"] is False:
            return "subtask deadline is not set"
        if sub_task["status"] is "null":
            return "subtask status is not set"
        if sub_task["priority"] is "null":
            return "subtask priority is not set"
        for part in sub_task["participants"]:
            if check_participants(part) is False:
                return "subtask participant is not set"
    for dependecy in task["dependencies"]:
        if sub_task["task-id"] is "null":
            return "subtask id is not set"
        if sub_task["deadline"] is False:
            return "subtask deadline is not set"
        if sub_task["status"] is "null":
            return "subtask status is not set"
        if sub_task["priority"] is "null":
            return "subtask priority is not set"
        for part in sub_task["participants"]:
            if check_participants(part) is False:
                return "subtask participant is not set"
    for reverse_dependecy in task["reverse-dependecies"]:
        if reverse_dependecy["task-id"] is "null":
            return "subtask id is not set"
        if reverse_dependecy["deadline"] is False:
            return "subtask deadline is not set"
        if reverse_dependecy["status"] is "null":
            return "subtask status is not set"
        if reverse_dependecy["priority"] is "null":
            return "subtask priority is not set"
        for part in reverse_dependecy["participants"]:
            if check_participants(part) is False:
                return "subtask participant is not set"
    for commit in task["commits"]:
        if commit["userId"] is "null":
            return "commit user id is not set"
        if commit["username"] is "null":
            return "commit username is not set"
        if commit["changes"] is "null":
            return "commit change is not set"
        if commit["date"] is "null":
            return "commit date is not set"
    
    post = {'nume': task["nume"], 'creare': task["creare"], 'expirare': task["expirare"]}
    post_id = coll.insert_one(post).inserted_id
    return str(post_id) + " was posted"


def put_task(task):
    coll.update(
        { '_id': ObjectId(task['_id']) },
        { "$set": { 'nume': task['nume'], 'creare': task['creare'], 'expirare': task['expirare'] } },
        upsert = False
    )
    return str(task['_id'])

def deleteById(id):
    deletedId = coll.find_one({"_id" : ObjectId(id)})
    deletedId["_id"] = str(deletedId["_id"])
    coll.remove({"_id" : ObjectId(id)})
    # result = {'a' : 'b'}
    return make_response(jsonify(""), 200)

