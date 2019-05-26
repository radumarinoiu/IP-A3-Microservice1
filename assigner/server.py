from flask import Flask
from flask import request
from flask_cors import CORS
import db

app = Flask(__name__)
CORS(app)


@app.route("/", methods=["GET"])
def get_all_tasks():
    return db.get_all()


@app.route("/<task_id>", methods=["GET"])
def get_task_by_id(task_id):
    return db.get_by_id(task_id)


@app.route("/", methods=["POST"])
def add_assignment():
    return db.post_assignment(request.get_json())


@app.route("/", methods=["PUT"])
def update_assignment():
    return db.put_assignment(request.get_json())


@app.route("/<task_id>", methods=["DELETE"])
def delete_by_id(task_id):
    return db.delete_by_id(task_id)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5122)
