from flask import Blueprint, request, jsonify, Response
from bson import ObjectId, json_util
from db import users_collection  # Import the MongoDB users collection
from flask_cors import CORS

# Create a Blueprint for task-related routes
tasks_bp = Blueprint("tasks", __name__)
CORS(tasks_bp)
# Route: Add a new tasklist for a specific user
@tasks_bp.route("/<user_id>/tasklists", methods=["POST"])
def add_tasklist(user_id):
    data = request.json
    users_collection.update_one(
        {"_id": ObjectId(user_id)},
        {"$push": {"tasklists": {"title": data["title"], "tasks": []}}}
    )
    return jsonify({"message": "Tasklist added"}), 201

# Route: Add a new task to a specific tasklist
@tasks_bp.route("/<user_id>/tasklists/<list_title>/tasks", methods=["POST"])
def add_task(user_id, list_title):
    data = request.json
    users_collection.update_one(
        {"_id": ObjectId(user_id), "tasklists.title": list_title},
        {"$push": {"tasklists.$.tasks": {"title": data["title"], "done": False}}}
    )
    return jsonify({"message": "Task added"}), 201

# Route: Mark a task as done
@tasks_bp.route("/<user_id>/tasklists/<list_title>/tasks/<task_title>/done", methods=["PATCH"])
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

# Route: Mark a task as not done (undo)
@tasks_bp.route("/<user_id>/tasklists/<list_title>/tasks/<task_title>/undone", methods=["PATCH"])
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

# Route: Delete a tasklist
@tasks_bp.route("/<user_id>/tasklists/<list_title>", methods=["DELETE"])
def delete_tasklist(user_id, list_title):
    result = users_collection.update_one(
        {"_id": ObjectId(user_id)},
        {"$pull": {"tasklists": {"title": list_title}}}
    )

    if result.modified_count == 0:
        return jsonify({"error": "Tasklist not found"}), 404

    return jsonify({"message": "Tasklist deleted successfully"}), 200

# Route: Delete a specific task from a tasklist
@tasks_bp.route("/<user_id>/tasklists/<list_title>/tasks/<task_title>", methods=["DELETE"])
def delete_task(user_id, list_title, task_title):
    result = users_collection.update_one(
        {"_id": ObjectId(user_id), "tasklists.title": list_title},
        {"$pull": {"tasklists.$.tasks": {"title": task_title}}}
    )

    if result.modified_count == 0:
        return jsonify({"error": "Task not found"}), 404

    return jsonify({"message": "Task deleted successfully"}), 200

# Route: Get all tasklists for a specific user
@tasks_bp.route("/<user_id>/tasklists", methods=["GET"])
def get_task_lists(user_id):
  user = users_collection.find_one({"_id": ObjectId(user_id)}, {"_id": 0, "tasklists": 1})
  if not user:
    return jsonify({"error": "User not found"}), 404
  return jsonify(user["tasklists"]), 200

