import json
import pymongo
import logging
import traceback

from pymongo import MongoClient
from bson.objectid import ObjectId
from bson.errors import InvalidId as InvalidIdException
from flask import jsonify
from jsonschema import validate

db_username = "devs"
db_password = "devs"

client = MongoClient("mongodb://{}:{}@localhost/admin".format(db_username, db_password))
db = client["microservice1"]
coll = db["tasks"]


with open("task_schema.json", "rb") as f:
    task_schema = json.load(f)


def getAll():
    tasks_list = list(coll.find({}))
    for task in tasks_list:
        task["_id"] = str(task["_id"])
    return jsonify(tasks_list), 200


def getById(task_id):
    try:
        task = coll.find_one({"_id" : ObjectId(task_id)})
    except InvalidIdException:
        return jsonify({"error": "Invalid id"}), 400
    if not task:
        return jsonify({}), 404
    else:
        task["_id"] = str(task["_id"])
        return jsonify(task), 200


def post_task(task):
    json_data, status_code = execute_post_action(task)
    return jsonify(json_data), status_code



def execute_post_action(task):
    if not task:
        return {"error": "Empty request."}, 400
    
    # Check task's fields
    if not check_object(task, task_schema):
        return {"error": "Invalid task format."}, 400

    if "sub-tasks" in task and task["sub-tasks"]:
        new_subtasks = []
        for subtask in task["sub-tasks"]:
            subtask_json_result, subtask_status_code = execute_post_action(subtask)
            if subtask_status_code == 201:
                new_subtasks += subtask_json_result["sub-tasks"]
            else:
                try_rolling_back_task_changes(new_subtasks)
                # TODO: This should be replaced with the proper recursive deletion if a task's subtasks should be removed on parent task removal.
                return subtask_json_result, subtask_status_code
        task["sub-tasks"] = new_subtasks
    post_id = coll.insert_one(task).inserted_id
    task["_id"] = str(post_id)
    return task, 201


def try_rolling_back_task_changes(task_id_list):
    for task_id in task_id_list:
        found = False
        try:
            found = bool(coll.find_one({"_id" : ObjectId(task_id)}))
            coll.remove({"_id" : ObjectId(task_id)})
        except:
            if found:
                logging.error("Failed rolling back changes with error:\n{}".format(traceback.format_exc()))
            else:
                logging.warning("Task missing so we failed rolling back changes with error:\n{}".format(traceback.format_exc()))


def put_task(task):
    if not task:
        return jsonify({"error": "Empty request."}), 400
    if "_id" not in task:
        return jsonify({"error": "Put request missing _id"}), 400
    
    # Check task's fields
    if not check_object(task, task_schema):
        return jsonify({"error": "Invalid task format."}), 400

    task["_id"] = ObjectId(task["_id"])
    coll.update(
        {"_id": task["_id"]},
        {"$set": task},
        upsert=False)
    task["_id"] = str(task["_id"])
    return jsonify(task), 200


def deleteById(task_id):
    deletedId = coll.find_one({"_id" : ObjectId(task_id)})
    deletedId["_id"] = str(deletedId["_id"])
    coll.remove({"_id" : ObjectId(task_id)})
    return jsonify({}), 200

def checkForUpdate(task_id):
    isCompleted = 0
    json_data = coll.find_one({"_id" : ObjectId(task_id)})
    json_data["_id"] = str(json_data["_id"])
    for data in json_data[0]['sub-tasks']:
        subTask = coll.find_one({"_id" : ObjectId(data['_id'])})
        subTask["_id"] = str(json_data["_id"])
        return jsonify(subTask), 200
    #     if(subTask['status'] == '1'):
    #         isCompleted = 1
    #     else:
    #         isCompleted = 0
    #         break
    # if(isCompleted == 1):
    #     json_data['status'] = '1'
    #     return jsonify({"task" : "Completed"}), 200
    # else:
    #     return jsonify({"task" : "Not Completed"}), 200
    

##################################### HELPER FUNCTIONS #####################################


def check_object(obj, schema):
    try:
        validate(instance=obj, schema=schema)
        return True
    except:
        logging.error(traceback.format_exc())
        return False
