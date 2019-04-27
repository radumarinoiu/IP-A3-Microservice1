from flask import Flask
from flask import request
import requests


# Constants

TASKS_MS_ADDRESS_PORT = "http://localhost:5121"
ASSIGNER_MS_ADDRESS_PORT = "http://localhost:5122"


# Initialization

app = Flask(__name__)


# Tasks Routes

@app.route("/tasks", methods = ["GET"])
def get_all_tasks():
    resp = requests.get(TASKS_MS_ADDRESS_PORT, stream=True)
    return resp.raw.read(), resp.status_code, resp.headers.items()

@app.route("/tasks/<task_id>", methods = ["GET"])
def get_task(task_id):
    resp = requests.get(TASKS_MS_ADDRESS_PORT + "/" + task_id)
    return resp.raw.read(), resp.status_code, resp.headers.items()

@app.route("/tasks", methods = ["POST"])
def add_task():
    resp = requests.post(TASKS_MS_ADDRESS_PORT, json=request.json)
    return resp.raw.read(), resp.status_code, resp.headers.items()

@app.route("/tasks/<task_id>", methods = ["PUT"])
def update_task(task_id):
    resp = requests.put(TASKS_MS_ADDRESS_PORT + "/" + task_id, json=request.json)
    return resp.raw.read(), resp.status_code, resp.headers.items()

@app.route("/tasks/<task_id>", methods = ["DELETE"])
def delete_task(task_id):
    resp = requests.delete(TASKS_MS_ADDRESS_PORT + "/" + task_id)
    return resp.raw.read(), resp.status_code, resp.headers.items()


# Assigner Routes

@app.route("/assigner", methods = ["GET"])
def get_all_assignments():
    resp = requests.get(ASSIGNER_MS_ADDRESS_PORT)
    return resp.raw.read(), resp.status_code, resp.headers.items()

@app.route("/assigner/<assignment_id>", methods = ["GET"])
def get_assignment(assignment_id):
    resp = requests.get(ASSIGNER_MS_ADDRESS_PORT + "/" + assignment_id)
    return resp.raw.read(), resp.status_code, resp.headers.items()

@app.route("/assigner", methods = ["POST"])
def add_assignment():
    print(request.json)
    resp = requests.post(ASSIGNER_MS_ADDRESS_PORT, json=request.json)
    return resp.raw.read(), resp.status_code, resp.headers.items()

@app.route("/assigner/<assignment_id>", methods = ["PUT"])
def update_assignment(assignment_id):
    resp = requests.put(ASSIGNER_MS_ADDRESS_PORT + "/" + assignment_id, json=request.json)
    return resp.raw.read(), resp.status_code, resp.headers.items()

@app.route("/assigner/<assignment_id>", methods = ["DELETE"])
def delete_assignment(task_id):
    resp = requests.delete(ASSIGNER_MS_ADDRESS_PORT + "/" + task_id)
    return resp.raw.read(), resp.status_code, resp.headers.items()


# Run App

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5123)
    app.debug = True
