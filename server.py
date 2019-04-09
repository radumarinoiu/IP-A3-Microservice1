from flask import Flask
import db

app = Flask(__name__)

@app.route("/")
def root():
    return db.getAll()
@app.route("/", methods = ["POST"])
def add_task():
	return db.post_task(request.get_json())

@app.route("/<id>")
def root_id(id):
    return db.getById(id)

@app.route("/", methods = ["PUT"])
def update_task():
	return db.put_task(request.get_json())



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5122)
