from flask import Blueprint, request, jsonify
import sqlite3
from datetime import datetime

attendance_bp = Blueprint("attendance_bp", __name__)

@attendance_bp.route("/attendance", methods=["POST"])
def mark_attendance():
    data = request.get_json()
    roll = data.get("roll")

    if not roll:
        return jsonify({"error": "Roll number required"}), 400

    conn = sqlite3.connect("attendance.db")
    cursor = conn.cursor()

    # Get student ID from roll
    cursor.execute("SELECT id FROM students WHERE roll = ?", (roll,))
    student = cursor.fetchone()

    if not student:
        conn.close()
        return jsonify({"error": "Student not found"}), 404

    student_id = student[0]
    today = datetime.now().strftime("%Y-%m-%d")

    # Prevent duplicate attendance same day
    cursor.execute("""
        SELECT * FROM attendance
        WHERE student_id = ? AND date = ?
    """, (student_id, today))

    already_marked = cursor.fetchone()

    if already_marked:
        conn.close()
        return jsonify({"message": "Attendance already marked today"}), 200

    # Insert attendance
    cursor.execute("""
        INSERT INTO attendance (student_id, date, status)
        VALUES (?, ?, ?)
    """, (student_id, today, "Present"))

    conn.commit()
    conn.close()

    return jsonify({"message": "Attendance marked successfully"})
