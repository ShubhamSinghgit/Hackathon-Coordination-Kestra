# src/routes.py
from flask import Blueprint, request, jsonify
import sqlite3
from .models import Task  # Change this line to use relative import

routes = Blueprint("routes", __name__)

@routes.route("/tasks", methods=["GET"])
def get_tasks():
    try:
        conn = sqlite3.connect("team_coordinator.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tasks")
        tasks = cursor.fetchall()
        return jsonify([dict(zip(['id', 'title', 'description', 'assigned_to', 'status', 'due_date'], task)) for task in tasks])
    except sqlite3.Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()

@routes.route("/tasks", methods=["POST"])
def create_task():
    try:
        data = request.json
        task = Task(
            title=data["title"],
            description=data.get("description"),
            assigned_to=data.get("assigned_to"),
            due_date=data.get("due_date")
        )
        
        conn = sqlite3.connect("team_coordinator.db")
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO tasks (title, description, assigned_to, due_date) VALUES (?, ?, ?, ?)", 
            (task.title, task.description, task.assigned_to, task.due_date)
        )
        conn.commit()
        return jsonify({"message": "Task created successfully!", "task_id": cursor.lastrowid}), 201
    except sqlite3.Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()