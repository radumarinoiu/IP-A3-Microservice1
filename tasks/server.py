from flask import Flask
from flask import request
import db

app = Flask(__name__)

@app.route("/")
def get_all_tasks():
    return db.getAll()

@app.route("/", methods = ["POST"])
def add_task():
    return db.post_task(request.get_json())

@app.route("/<task_id>")
def get_task_by_id(task_id):
    return db.getById(task_id)

@app.route("/<task_id>", methods = ["DELETE"])
def delete_task(task_id):
    return db.deleteById(task_id)

@app.route("/", methods = ["PUT"])
def update_task():
    return db.put_task(request.get_json())



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5121)
