from flask import Blueprint, request, jsonify
import sqlite3

teacher_bp = Blueprint("teacher_bp", __name__)

# Register Teacher
@teacher_bp.route("/teachers", methods=["POST"])
def add_teacher():
    data = request.get_json()
    name = data.get("name")
    email = data.get("email")
    password = data.get("password")

    if not name or not email or not password:
        return jsonify({"error": "All fields required"}), 400

    conn = sqlite3.connect(
    r"C:\Users\PABITRA KUMAR BARIK\OneDrive\SmartAttend AI 1\attendance.db"
)

    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO teachers (name, email, password)
            VALUES (?, ?, ?)
        """, (name, email, password))
        conn.commit()
    except sqlite3.IntegrityError:
        conn.close()
        return jsonify({"error": "Teacher already exists"}), 400

    conn.close()
    return jsonify({"message": "Teacher registered successfully"})


# Simple Login
@teacher_bp.route("/teacher/login", methods=["POST"])
def teacher_login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    conn = sqlite3.connect(
    r"C:\Users\PABITRA KUMAR BARIK\OneDrive\SmartAttend AI 1\attendance.db"
)

    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, name FROM teachers
        WHERE email = ? AND password = ?
    """, (email, password))

    teacher = cursor.fetchone()
    conn.close()

    if not teacher:
        return jsonify({"error": "Invalid credentials"}), 401

    return jsonify({
        "message": "Login successful",
        "teacher_id": teacher[0],
        "teacher_name": teacher[1]
    })
