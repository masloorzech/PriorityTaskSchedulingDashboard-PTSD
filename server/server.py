import datetime

from bson import json_util, ObjectId
from flask import Flask, request, jsonify, Response
from pymongo import MongoClient
import bcrypt

app = Flask(__name__)

client = MongoClient("mongodb://admin:admin123@localhost:27017/")
db = client["task_manager"]
users_collection = db["users"]
task_lists_collection = db["task_lists"]
tasks_collection = db["tasks"]

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
    users_collection.insert_one({"username": username, "password": hashed_password})

    return jsonify({"message": "User registered successfully"}), 201

@app.route("/create_task_list", methods=["POST"])
def create_task_list():
    data = request.get_json()
    user_id = data.get("user_id")
    list_name = data.get("list_name")
    if not user_id or not list_name:
        return jsonify({"error": "User ID and list name are required"}), 400

    new_list = {
        "user_id": ObjectId(user_id),
        "name": list_name,
    }
    result = task_lists_collection.insert_one(new_list)
    return jsonify({"message": "Task list created successfully", "list_id": str(result.inserted_id)}), 201


@app.route("/get_task_lists/<user_id>", methods=["GET"])
def get_task_lists(user_id):
    lists = list(task_lists_collection.find({"user_id": ObjectId(user_id)}))
    for task_list in lists:
        task_list["_id"] = str(task_list["_id"])
        task_list["user_id"] = str(task_list["user_id"])

    return jsonify(lists), 200


if __name__ == "__main__":
    app.run(debug=True)
