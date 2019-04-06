from flask import Flask
import db
app = Flask(__name__)

@app.route("/")
def root():
    return db.getAll()

@app.route("/<id>")
def root_id(id):
    return db.getById(id)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5122)
