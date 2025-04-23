from pymongo import MongoClient

client = None
db = None
users_collection = None

def db_init():
    global client, db, users_collection
    client = MongoClient("mongodb://admin:admin123@localhost:27017/")
    db = client["task_manager"]
    users_collection = db["users"]
