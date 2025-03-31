from pymongo import MongoClient

client = MongoClient("mongodb://127.0.0.1:27017/")

db = client["task_manager"]

collections = db.list_collection_names()

if "users" not in collections:
    db.create_collection("users")
    print("Kolekcja 'users' została utworzona.")
else:
    print("Kolekcja 'users' już istnieje.")

if "tasks" not in collections:
    db.create_collection("tasks")
    print("Kolekcja 'tasks' została utworzona.")
else:
    print("Kolekcja 'tasks' już istnieje.")
