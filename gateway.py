from flask import Flask
from flask import request
import requests


# Constants

TASKS_MS_ADDRESS_PORT = "localhost:5121"
ASSIGNER_MS_ADDRESS_PORT = "localhost:5122"


# Initialization

app = Flask(__name__)


# Tasks Routes

@app.route("/tasks", methods = ["GET"])
def get_all_tasks():
    return requests.get(TASKS_MS_ADDRESS_PORT)

@app.route("/tasks/<task_id>", methods = ["GET"])
def get_task(task_id):
    return requests.get(TASKS_MS_ADDRESS_PORT + "/" + task_id)

@app.route("/tasks", methods = ["POST"])
def add_task():
    return requests.post(TASKS_MS_ADDRESS_PORT, request.json)

@app.route("/tasks/<task_id>", methods = ["PUT"])
def update_task(task_id):
    return requests.put(TASKS_MS_ADDRESS_PORT + "/" + task_id, request.json)

@app.route("/tasks/<task_id>", methods = ["DELETE"])
def delete_task(task_id):
    return requests.delete(TASKS_MS_ADDRESS_PORT + "/" + task_id)


# Assigner Routes

@app.route("/assigner", methods = ["GET"])
def get_all_assignments():
    return requests.get(TASKS_MS_ADDRESS_PORT)

@app.route("/assigner/<assignment_id>", methods = ["GET"])
def get_assignment(assignment_id):
    return requests.get(TASKS_MS_ADDRESS_PORT + "/" + assignment_id)

@app.route("/assigner", methods = ["POST"])
def add_assignment():
    return requests.post(TASKS_MS_ADDRESS_PORT, request.json)

@app.route("/assigner/<assignment_id>", methods = ["PUT"])
def update_assignment(assignment_id):
    return requests.put(TASKS_MS_ADDRESS_PORT + "/" + assignment_id, request.json)

@app.route("/assigner/<assignment_id>", methods = ["DELETE"])
def delete_assignment(task_id):
    return requests.delete(TASKS_MS_ADDRESS_PORT + "/" + task_id)


# Run App

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5123)
    app.debug = True
