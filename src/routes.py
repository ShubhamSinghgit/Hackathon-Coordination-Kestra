from flask import Blueprint, request, jsonify
import sqlite3

routes = Blueprint("routes", __name__)

@routes.route("/tasks", methods=["GET"])
def get_tasks():
    conn = sqlite3.connect("team_coordinator.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks")
    tasks = cursor.fetchall()
    conn.close()
    return jsonify(tasks)

@routes.route("/tasks", methods=["POST"])
def create_task():
    data = request.json
    conn = sqlite3.connect("team_coordinator.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO tasks (title, description, assigned_to, due_date) VALUES (?, ?, ?, ?)", 
                   (data["title"], data["description"], data["assigned_to"], data["due_date"]))
    conn.commit()
    conn.close()
    return jsonify({"message": "Task created successfully!"}), 201
