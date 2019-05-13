from flask import Flask
from flask import request
import db

app = Flask(__name__)

@app.route("/")
def get_sorted_tasks():
    return db.sortTasks(request.json)




if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5124)
