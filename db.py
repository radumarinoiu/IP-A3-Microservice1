from pymongo import MongoClient

db_username = "devs"
db_password = "devs"

client = MongoClient("mongodb://{}:{}@localhost/tasks_db".format(db_username, db_password))
tasks_db = client["tasks_db"] # This is the database
tasks = tasks_db["tasks"] # This is a collection (table) in the database

def test():
    return "Test works!"
