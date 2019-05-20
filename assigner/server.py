from flask import Flask
from flask import request
from flask_cors import CORS
import db

app = Flask(__name__)
CORS(app)

@app.route("/")
def get_all_tasks():
    return db.getAll()

@app.route("/", methods = ["POST"])
def add_assignement():
    return db.post_assignement(request.get_json())

@app.route("/<id>")
def get_task_by_id(task_id):
    return db.getById(task_id)

@app.route("/", methods = ["PUT"])
def update_assignement():
    return db.put_assignement(request.get_json())



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5122)
