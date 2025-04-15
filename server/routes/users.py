from flask import Blueprint, request, jsonify, Response
from bson import ObjectId, json_util
from db import users_collection
import bcrypt


def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode(), salt)
    return hashed.decode()

users_bp = Blueprint("users", __name__)


@users_bp.route('/users', methods=['GET'])
def get_users():
    users = users_collection.find()
    users_list = list(users)
    return Response(json_util.dumps({"data": users_list}), mimetype="application/json")


@users_bp.route('/delete_user', methods=['POST'])
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


@users_bp.route("/get_user_id", methods=["POST"])
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


@users_bp.route("/user_exist", methods=["POST"])
def user_exist():
    data = request.get_json()
    username = data["username"]
    if not username:
        return jsonify({"error": "Username is required"}), 400

    user = users_collection.find_one({"username": username})
    if user:
        return jsonify({"exists": True}), 200
    return jsonify({"exists": False}), 200


@users_bp.route("/log_in", methods=["POST"])
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


@users_bp.route("/register", methods=["POST"])
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