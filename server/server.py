from flask import Flask, request, jsonify
from pymongo import MongoClient
import bcrypt

app = Flask(__name__)

client = MongoClient("mongodb://localhost:27017/")
db = client["task_manager"]
users_collection = db["users"]


def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode(), salt)
    return hashed.decode()


@app.route("/")
def index():
    return "connected"


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

    return jsonify({"logged_in": True}), 200
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


if __name__ == "__main__":
    app.run(debug=True)
