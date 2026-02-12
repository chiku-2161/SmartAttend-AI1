from flask import Blueprint, jsonify
import sqlite3
from smart_attendance_system.services.risk_engine import calculate_risk
from smart_attendance_system.services.forecast_engine import forecast_attendance

# 🔥 DEFINE BLUEPRINT FIRST
analytics_bp = Blueprint("analytics_bp", __name__)


# -------------------------------
# STUDENT ANALYTICS
# -------------------------------
@analytics_bp.route("/analytics/student/<int:student_id>", methods=["GET"])
def student_analytics(student_id):
    conn = sqlite3.connect(
    r"C:\Users\PABITRA KUMAR BARIK\OneDrive\SmartAttend AI 1\attendance.db"
)

    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM attendance WHERE student_id = ?", (student_id,))
    total_classes = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*) FROM attendance
        WHERE student_id = ? AND status = 'Present'
    """, (student_id,))
    presents = cursor.fetchone()[0]

    attendance_percentage = 0
    if total_classes > 0:
        attendance_percentage = (presents / total_classes) * 100

    risk_level = calculate_risk(attendance_percentage)
    forecast_percentage = forecast_attendance(presents, total_classes, 5)

    conn.close()

    return jsonify({
        "success": True,
        "data": {
            "student_id": student_id,
            "total_classes": total_classes,
            "present_classes": presents,
            "attendance_percentage": round(attendance_percentage, 2),
            "risk_level": risk_level,
            "forecast_next_5_classes": round(forecast_percentage, 2)
        },
        "message": "Student analytics fetched"
    })


# -------------------------------
# SECTION ANALYTICS
# -------------------------------
@analytics_bp.route("/analytics/section/<int:section_id>", methods=["GET"])
def section_analytics(section_id):
    conn = sqlite3.connect(
    r"C:\Users\PABITRA KUMAR BARIK\OneDrive\SmartAttend AI 1\attendance.db"
)

    cursor = conn.cursor()

    cursor.execute("SELECT id FROM students WHERE section_id = ?", (section_id,))
    students = cursor.fetchall()

    total_students = len(students)
    risk_summary = {"Low": 0, "Medium": 0, "High": 0}

    for student in students:
        student_id = student[0]

        cursor.execute("SELECT COUNT(*) FROM attendance WHERE student_id = ?", (student_id,))
        total = cursor.fetchone()[0]

        cursor.execute("""
            SELECT COUNT(*) FROM attendance
            WHERE student_id = ? AND status = 'Present'
        """, (student_id,))
        present = cursor.fetchone()[0]

        percentage = 0
        if total > 0:
            percentage = (present / total) * 100

        risk = calculate_risk(percentage)
        risk_summary[risk] += 1

    conn.close()

    return jsonify({
        "success": True,
        "data": {
            "section_id": section_id,
            "total_students": total_students,
            "risk_distribution": risk_summary
        },
        "message": "Section analytics fetched"
    })

@analytics_bp.route("/analytics/dashboard", methods=["GET"])
def dashboard_summary():
    conn = sqlite3.connect(
        r"C:\Users\PABITRA KUMAR BARIK\OneDrive\SmartAttend AI 1\attendance.db"
    )
    cursor = conn.cursor()

    # Total students
    cursor.execute("SELECT COUNT(*) FROM students")
    total_students = cursor.fetchone()[0]

    # Total attendance records
    cursor.execute("SELECT COUNT(*) FROM attendance")
    total_records = cursor.fetchone()[0]

    # Present count
    cursor.execute("SELECT COUNT(*) FROM attendance WHERE status = 'Present'")
    total_present = cursor.fetchone()[0]

    # Average attendance %
    average_attendance = 0
    if total_records > 0:
        average_attendance = (total_present / total_records) * 100

    # ---------------- RISK DISTRIBUTION (STATUS BASED) ----------------
    cursor.execute("""
        SELECT status, COUNT(*)
        FROM attendance
        GROUP BY status
    """)
    rows = cursor.fetchall()

    risk_summary = {"Low": 0, "Medium": 0, "High": 0}

    for status, count in rows:
        if status == "Absent":
            risk_summary["High"] += count
        elif status == "Late":
            risk_summary["Medium"] += count
        elif status == "Present":
            risk_summary["Low"] += count

    conn.close()

    return jsonify({
        "success": True,
        "data": {
            "total_students": total_students,
            "average_attendance_percentage": round(average_attendance, 2),
            "risk_distribution": risk_summary
        },
        "message": "Dashboard analytics fetched"
    })

@analytics_bp.route("/debug/attendance/<int:session_id>")
def debug_attendance(session_id):
    conn = sqlite3.connect(
        r"C:\Users\PABITRA KUMAR BARIK\OneDrive\SmartAttend AI 1\attendance.db"
    )
    cursor = conn.cursor()

    cursor.execute("""
        SELECT student_id, status
        FROM attendance
        WHERE session_id = ?
    """, (session_id,))

    rows = cursor.fetchall()
    conn.close()

    return jsonify(rows)


@analytics_bp.route("/debug/students")
def debug_students():
    conn = sqlite3.connect(
    r"C:\Users\PABITRA KUMAR BARIK\OneDrive\SmartAttend AI 1\attendance.db"
)

    cursor = conn.cursor()

    cursor.execute("SELECT id, name FROM students")
    rows = cursor.fetchall()
    conn.close()

    return jsonify(rows)
