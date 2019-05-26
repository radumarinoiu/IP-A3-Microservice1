import pymongo
import json
from jsonschema import validate

from pymongo import MongoClient
from bson.objectid import ObjectId
from flask import jsonify

db_username = "devs"
db_password = "devs"

client = MongoClient("mongodb://{}:{}@localhost/admin".format(db_username, db_password))
db = client["microservice1"]
coll = db["assigner"]

with open("assigner_schema.json", "rb") as f:
    assignment_schema = json.load(f)


def get_all():
    get_all_list = list(coll.find({}))
    for task in get_all_list:
        task["_id"] = str(task["_id"])
    return jsonify(get_all_list), 200


def get_by_id(obj_id):
    obj = coll.find_one({"_id": ObjectId(obj_id)})
    if not obj:
        return jsonify({}), 404
    obj["_id"] = str(obj["_id"])
    return jsonify(obj), 200


def post_assignment(assignment):
    if not assignment:
        return jsonify({"error": "Empty request."}), 400
    if not check_object(assignment, assignment_schema):
        return {"error": "Invalid task format."}, 400

    post_id = coll.insert_one(assignment).inserted_id
    assignment["_id"] = str(post_id)
    return jsonify(assignment), 201


def put_assignment(assignment):
    if not assignment:
        return jsonify({"error": "Empty request."}), 400
    if "_id" not in assignment:
        return jsonify({"error": "Put request missing _id"}), 400
    assignment_id = assignment.pop("_id")
    # Check task's fields
    if not check_object(assignment, assignment_schema):
        return jsonify({"error": "Invalid assignment format."}), 400

    assignment["_id"] = ObjectId(assignment_id)
    coll.update(
        {"_id": assignment["_id"]},
        {"$set": assignment},
        upsert=False)
    assignment["_id"] = str(assignment["_id"])
    return jsonify(assignment), 200


def delete_by_id(assignment_id):
    obj = coll.find_one({"_id": ObjectId(assignment_id)})
    if not obj:
        return jsonify({}), 404
    coll.remove({"_id": ObjectId(assignment_id)})
    return jsonify({}), 200


def check_object(obj, schema):
    try:
        validate(instance=obj, schema=schema)
        return True
    except Exception:
        return False
