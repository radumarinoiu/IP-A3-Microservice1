from flask import Flask
import create_task
import requests

app = Flask(__name__)

@app.route("/", methods = ["POST"])
def add_task():
	return create_task.post_task(request.get_json())

@app.route("/", methods = ["PUT"])
def update_task():
	return create_task.put_task(request.get_json())



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5123)
