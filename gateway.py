from flask import Flask, request, jsonify
import requests


# Constants

TASKS_MS_ADDRESS_PORT = "http://localhost:5121"
ASSIGNER_MS_ADDRESS_PORT = "http://localhost:5122"
SORTER_MS_ADDRESS_PORT = "http://localhost:5124"


# Initialization

app = Flask(__name__)


# Tasks Routes

@app.route("/tasks", methods = ["GET"])
def get_all_tasks():
    resp = requests.get(TASKS_MS_ADDRESS_PORT, stream=True)
    return resp.raw.read(), resp.status_code, resp.headers.items()

@app.route("/tasks/<task_id>", methods = ["GET"])
def get_task(task_id):
    resp = requests.get(TASKS_MS_ADDRESS_PORT + "/" + task_id, stream=True)
    return resp.raw.read(), resp.status_code, resp.headers.items()

@app.route("/tasks", methods = ["POST"])
def add_task():
    resp = requests.post(TASKS_MS_ADDRESS_PORT, json=request.json, stream=True)
    return resp.raw.read(), resp.status_code, resp.headers.items()

@app.route("/tasks", methods = ["PUT"])
def update_task():
    resp = requests.put(TASKS_MS_ADDRESS_PORT, json=request.json, stream=True)
    return resp.raw.read(), resp.status_code, resp.headers.items()

@app.route("/tasks/<task_id>", methods = ["DELETE"])
def delete_task(task_id):
    resp = requests.delete(TASKS_MS_ADDRESS_PORT + "/" + task_id, stream=True)
    return resp.raw.read(), resp.status_code, resp.headers.items()


# Assigner Routes

@app.route("/assigner", methods = ["GET"])
def get_all_assignments():
    resp = requests.get(ASSIGNER_MS_ADDRESS_PORT, stream=True)
    return resp.raw.read(), resp.status_code, resp.headers.items()

@app.route("/assigner/<assignment_id>", methods = ["GET"])
def get_assignment(assignment_id):
    resp = requests.get(ASSIGNER_MS_ADDRESS_PORT + "/" + assignment_id, stream=True)
    return resp.raw.read(), resp.status_code, resp.headers.items()

@app.route("/assigner", methods = ["POST"])
def add_assignment():
    resp = requests.post(ASSIGNER_MS_ADDRESS_PORT, json=request.json, stream=True)
    return resp.raw.read(), resp.status_code, resp.headers.items()

@app.route("/assigner/<assignment_id>", methods = ["PUT"])
def update_assignment(assignment_id):
    resp = requests.put(ASSIGNER_MS_ADDRESS_PORT + "/" + assignment_id, json=request.json, stream=True)
    return resp.raw.read(), resp.status_code, resp.headers.items()

@app.route("/assigner/<assignment_id>", methods = ["DELETE"])
def delete_assignment(task_id):
    resp = requests.delete(ASSIGNER_MS_ADDRESS_PORT + "/" + task_id, stream=True)
    return resp.raw.read(), resp.status_code, resp.headers.items()


# Sorter Routes

@app.route("/sorter/<user_id>", methods = ["GET"])
def get_sorted_tasks_for_user(user_id):
    if not request.json:
        return jsonify({"error": "Empty request."}), 400
    if "preferences" not in request.json:
        return jsonify({"error": "Preferences missing"}), 400
    sort_obj = {"preferences": request.json["preferences"]}
    # Get the ids of the user's assigned tasks
    resp = requests.get(ASSIGNER_MS_ADDRESS_PORT, stream=True)
    if resp.status_code != 200:
        return resp.raw.read(), resp.status_code, resp.headers.items()
    assignments = resp.json()
    user_task_ids = []
    for assignment in assignments:
        if user_id == assignment["id_user"]:
            user_task_ids.append(assignment["id_task"])

    # Get all the tasks by id and put them in a list
    user_tasks = []
    for task_id in user_task_ids:
        resp = requests.get(TASKS_MS_ADDRESS_PORT + "/" + task_id, stream=True)
        if resp.status_code != 200:
            return resp.raw.read(), resp.status_code, resp.headers.items()
        task = resp.json()
        user_tasks.append(task)
    sort_obj["tasks"] = user_tasks

    # Get sorted tasks for today
    resp = requests.get(SORTER_MS_ADDRESS_PORT, json=sort_obj, stream=True)
    return resp.raw.read(), resp.status_code, resp.headers.items()


# Run App

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5123)
    app.debug = True
