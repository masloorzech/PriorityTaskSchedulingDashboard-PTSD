import datetime

from bson import json_util, ObjectId
from flask import Flask, request, jsonify, Response
from pymongo import MongoClient
import bcrypt

app = Flask(__name__)

client = MongoClient("mongodb://admin:admin123@localhost:27017/")
db = client["task_manager"]
users_collection = db["users"]

def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode(), salt)
    return hashed.decode()

@app.route('/users', methods=['GET'])
def get_users():
    users = users_collection.find()
    users_list = list(users)  # Convert the cursor to a list
    return Response(json_util.dumps({"data": users_list}), mimetype="application/json")
@app.route("/")
def index():
    return "connected"

@app.route('/delete_user', methods=['POST'])
def delete_user():
    data = request.get_json()
    admin_id = data["admin_id"]
    user_id = data["user_id"]
    if not user_id or not admin_id:
        return jsonify({"error": "Admin and user id's are required"}), 400
    if user_id == admin_id:
        return jsonify({"error": "Cannot delete administrator account"}), 200
    admin_user = users_collection.find_one({"username": "ADMIN"})
    if admin_user["_id"] != ObjectId(admin_id):
        return jsonify({"error": "Unauthorized: Only admin can delete users"}), 403
    user = users_collection.find_one({"_id": ObjectId(user_id)})
    if not user:
        return jsonify({"error": "User not found"}), 404
    users_collection.delete_one({"_id": ObjectId(user_id)})
    return jsonify({"success": True})

@app.route("/get_user_id", methods=["POST"])
def get_user_id():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Missing username or password"}), 400

    user = users_collection.find_one({"username": username})
    if not user:
        return jsonify({"error": "User not found"}), 404

    if not bcrypt.checkpw(password.encode(), user["password"].encode()):
        return jsonify({"error": "Incorrect password"}), 401

    return jsonify({"user_id": str(user["_id"])}), 200

@app.route("/user_exist", methods=["POST"])
def user_exist():
    data = request.get_json()
    username = data["username"]
    if not username:
        return jsonify({"error": "Username is required"}), 400

    user = users_collection.find_one({"username": username})
    if user:
        return jsonify({"exists": True}), 200
    return jsonify({"exists": False}), 200

@app.route("/log_in", methods=["POST"])
def log_in():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if not username:
        return jsonify({"error": "Username is required"}), 400
    if not password:
        return jsonify({"error": "Password is required"}), 400

    user = users_collection.find_one({"username": username})
    if not user:
        return jsonify({"error": "User not found"}), 404

    if not bcrypt.checkpw(password.encode(), user["password"].encode()):
        return jsonify({"error": "Incorrect password"}), 401

    return jsonify({"logged_in": True, "user_id":str(user["_id"])}), 200
@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Missing username or password"}), 400

    if users_collection.find_one({"username": username}):
        return jsonify({"error": "User already exists"}), 400

    hashed_password = hash_password(password)
    user = {
      "username": username,
      "password": hashed_password,
      "tasklists": []
    }
    users_collection.insert_one(user)

    return jsonify({"message": "User registered successfully"}), 201

@app.route("/users/<user_id>/tasklists", methods=["POST"])
def add_tasklist(user_id):
    data = request.json  # { "title": "new list example" }
    users_collection.update_one(
        {"_id": ObjectId(user_id)},
        {"$push": {"tasklists": {"title": data["title"], "tasks": []}}}
    )
    return jsonify({"message": "Tasklist added"}), 201

@app.route("/users/<user_id>/tasklists/<list_title>/tasks", methods=["POST"])
def add_task(user_id, list_title):
    data = request.json  # { "title": "Nowe zadanie" }
    users_collection.update_one(
        {"_id": ObjectId(user_id), "tasklists.title": list_title},
        {"$push": {"tasklists.$.tasks": {"title": data["title"], "done": False}}}
    )
    return jsonify({"message": "Task added"}), 201

@app.route("/users/<user_id>/tasklists/<list_title>/tasks/<task_title>/done", methods=["PATCH"])
def mark_task_done(user_id, list_title, task_title):
    users_collection.update_one(
        {"_id": ObjectId(user_id), "tasklists.title": list_title},
        {
            "$set": {"tasklists.$[list].tasks.$[task].done": True}
        },
        array_filters=[
            {"list.title": list_title},
            {"task.title": task_title}
        ]
    )
    return jsonify({"message": "Task marked as done"}), 200

@app.route("/users/<user_id>/tasklists/<list_title>/tasks/<task_title>/undone", methods=["PATCH"])
def mark_task_undone(user_id, list_title, task_title):
    users_collection.update_one(
        {"_id": ObjectId(user_id), "tasklists.title": list_title},
        {
            "$set": {"tasklists.$[list].tasks.$[task].done": False}
        },
        array_filters=[
            {"list.title": list_title},
            {"task.title": task_title}
        ]
    )
    return jsonify({"message": "Task marked as done"}), 200



@app.route("/users/<user_id>/tasklists", methods=["GET"])
def get_task_lists(user_id):
  user = users_collection.find_one({"_id": ObjectId(user_id)}, {"_id": 0, "tasklists": 1})

  if not user:
    return jsonify({"error": "User not found"}), 404

  return jsonify(user["tasklists"]), 200


if __name__ == "__main__":
    app.run(debug=True)
