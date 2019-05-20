from flask import Flask
from flask import request
from flask_cors import CORS
import db

app = Flask(__name__)
CORS(app)

@app.route("/")
def get_sorted_tasks():
    return db.sortTasks(request.json)




if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5124)
