from flask import Blueprint, request, jsonify
import sqlite3

student_bp = Blueprint("student_bp", __name__)


# -----------------------------
# ADD STUDENT
# -----------------------------
@student_bp.route("/students", methods=["POST"])
def add_student():
    data = request.get_json()

    name = data.get("name")
    roll = data.get("roll")
    section_id = data.get("section_id")

    if not name or not roll or not section_id:
        return jsonify({
            "success": False,
            "error": "Name, roll and section_id required"
        }), 400

    conn = sqlite3.connect("attendance.db")
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO students (name, roll, section_id)
            VALUES (?, ?, ?)
        """, (name, roll, section_id))

        conn.commit()
    except sqlite3.IntegrityError:
        conn.close()
        return jsonify({
            "success": False,
            "error": "Student already exists"
        }), 400

    conn.close()

    return jsonify({
        "success": True,
        "message": "Student added successfully"
    })
