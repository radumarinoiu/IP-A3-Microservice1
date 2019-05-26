import db
import logging

from flask import Flask
from flask import request
from flask import make_response

logging.basicConfig(filename="tasks.log", level=logging.DEBUG, filemode="w")

app = Flask(__name__)

@app.route("/", methods = ["GET"])
def get_all_tasks():
    return db.getAll()

@app.route("/", methods = ["POST"])
def add_task():
    if not request.is_json:
        return {"error": "Request is not a valid json."}, 400
    return db.post_task(request.json)

@app.route("/<task_id>", methods = ["GET"])
def get_task_by_id(task_id):
    return db.getById(task_id)

@app.route("/<task_id>", methods = ["DELETE"])
def delete_task(task_id):
    return db.deleteById(task_id)

@app.route("/", methods = ["PUT"])
def update_task():
    if not request.is_json:
        return {"error": "Request is not a valid json."}, 400
    return db.put_task(request.json)

@app.route("/check/<task_id>", methods = ["GET"])
def check_task(task_id):
    return db.checkForUpdate(task_id)



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5125)
