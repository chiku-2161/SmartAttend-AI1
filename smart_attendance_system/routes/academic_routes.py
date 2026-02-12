import csv
import os
from flask import Blueprint, request, jsonify
import sqlite3
from datetime import datetime

academic_bp = Blueprint("academic_bp", __name__)

# --------------------------------------------------
# CREATE SECTION
# --------------------------------------------------
@academic_bp.route("/sections", methods=["POST"])
def create_section():
    data = request.get_json()
    name = data.get("name")
    department = data.get("department")
    year = data.get("year")

    if not name:
        return jsonify({"success": False, "error": "Section name required"}), 400

    conn =  sqlite3.connect(
    r"C:\Users\PABITRA KUMAR BARIK\OneDrive\SmartAttend AI 1\attendance.db"
)

    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO sections (name, department, year)
        VALUES (?, ?, ?)
    """, (name, department, year))

    conn.commit()
    conn.close()

    return jsonify({"success": True, "message": "Section created successfully"})


# --------------------------------------------------
# CREATE SUBJECT
# --------------------------------------------------
@academic_bp.route("/subjects", methods=["POST"])
def create_subject():
    data = request.get_json()
    name = data.get("name")
    code = data.get("code")

    if not name or not code:
        return jsonify({"success": False, "error": "Name and code required"}), 400

    conn = sqlite3.connect(
    r"C:\Users\PABITRA KUMAR BARIK\OneDrive\SmartAttend AI 1\attendance.db"
)

    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO subjects (name, code)
            VALUES (?, ?)
        """, (name, code))
        conn.commit()
    except sqlite3.IntegrityError:
        conn.close()
        return jsonify({"success": False, "error": "Subject already exists"}), 400

    conn.close()

    return jsonify({"success": True, "message": "Subject created successfully"})


# --------------------------------------------------
# CREATE ASSIGNMENT
# --------------------------------------------------
@academic_bp.route("/assignments", methods=["POST"])
def create_assignment():
    data = request.get_json()
    teacher_id = data.get("teacher_id")
    subject_id = data.get("subject_id")
    section_id = data.get("section_id")

    if not teacher_id or not subject_id or not section_id:
        return jsonify({"success": False, "error": "All IDs required"}), 400

    conn = sqlite3.connect(
    r"C:\Users\PABITRA KUMAR BARIK\OneDrive\SmartAttend AI 1\attendance.db"
    )
    cursor = conn.cursor()


    cursor.execute("""
        INSERT INTO subject_assignments (teacher_id, subject_id, section_id)
        VALUES (?, ?, ?)
    """, (teacher_id, subject_id, section_id))

    conn.commit()
    conn.close()

    return jsonify({"success": True, "message": "Assignment created successfully"})


# --------------------------------------------------
# GET TEACHER ASSIGNMENTS
# --------------------------------------------------
@academic_bp.route("/teacher/<int:teacher_id>/assignments", methods=["GET"])
def get_teacher_assignments(teacher_id):
    conn = sqlite3.connect(
    r"C:\Users\PABITRA KUMAR BARIK\OneDrive\SmartAttend AI 1\attendance.db"
)

    cursor = conn.cursor()

    cursor.execute("""
        SELECT sa.id, s.name, s.code, sec.name
        FROM subject_assignments sa
        JOIN subjects s ON sa.subject_id = s.id
        JOIN sections sec ON sa.section_id = sec.id
        WHERE sa.teacher_id = ?
    """, (teacher_id,))

    assignments = cursor.fetchall()
    conn.close()

    result = []
    for a in assignments:
        result.append({
            "assignment_id": a[0],
            "subject_name": a[1],
            "subject_code": a[2],
            "section_name": a[3]
        })

    return jsonify({"success": True, "assignments": result})


# --------------------------------------------------
# TEACHER START CLASS (BOOTSTRAP SESSION)
# --------------------------------------------------
@academic_bp.route("/teacher/start-class", methods=["POST"])

def teacher_start_class():
    data = request.get_json()
    teacher_id = data.get("teacher_id")
    assignment_id = data.get("assignment_id")

    if not teacher_id or not assignment_id:
        return jsonify({
            "success": False,
            "error": "Teacher ID and Assignment ID required"
        }), 400

    conn = sqlite3.connect(
    r"C:\Users\PABITRA KUMAR BARIK\OneDrive\SmartAttend AI 1\attendance.db"
)

    cursor = conn.cursor()

    # Validate teacher owns assignment
    cursor.execute("""
        SELECT section_id 
        FROM subject_assignments
        WHERE id = ? AND teacher_id = ?
    """, (assignment_id, teacher_id))

    assignment = cursor.fetchone()

    if not assignment:
        conn.close()
        return jsonify({
            "success": False,
            "error": "Invalid assignment for this teacher"
        }), 400

    section_id = assignment[0]

    start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Create session
    cursor.execute("""
        INSERT INTO class_sessions (subject_assignment_id, start_time, status)
        VALUES (?, ?, ?)
    """, (assignment_id, start_time, "active"))

    session_id = cursor.lastrowid

    # Load students
    cursor.execute("""
        SELECT id FROM students
        WHERE section_id = ?
    """, (section_id,))

    students = cursor.fetchall()

    for student in students:
        cursor.execute("""
            INSERT INTO presence_scores (student_id, session_id, points)
            VALUES (?, ?, 0)
        """, (student[0], session_id))

    conn.commit()
    conn.close()

    return jsonify({
        "success": True,
        "message": "Class session started",
        "session_id": session_id
    })


# --------------------------------------------------
# SAFE INCREMENT
# --------------------------------------------------
@academic_bp.route("/session/increment", methods=["POST"])
def increment_presence():
    data = request.get_json()
    session_id = data.get("session_id")
    student_id = data.get("student_id")

    if not session_id or not student_id:
        return jsonify({
            "success": False,
            "error": "Session ID and Student ID required"
        }), 400

    conn = sqlite3.connect(
    r"C:\Users\PABITRA KUMAR BARIK\OneDrive\SmartAttend AI 1\attendance.db"
)

    cursor = conn.cursor()

    # 🔒 Check if session is active
    cursor.execute("""
        SELECT status FROM class_sessions
        WHERE id = ?
    """, (session_id,))

    session = cursor.fetchone()

    if not session or session[0] != "active":
        conn.close()
        return jsonify({
            "success": False,
            "error": "Session is not active"
        }), 400

    # ✅ Increment points
    cursor.execute("""
        UPDATE presence_scores
        SET points = points + 1
        WHERE session_id = ? AND student_id = ?
    """, (session_id, student_id))

    conn.commit()
    conn.close()

    return jsonify({
        "success": True,
        "message": "Presence point incremented"
    })



# -----------------------------
# END SESSION
# -----------------------------
@academic_bp.route("/session/end", methods=["POST"])
def end_session():
    data = request.get_json()
    session_id = data.get("session_id")
    total_intervals = data.get("total_intervals")

    if not session_id or not total_intervals:
        return jsonify({
            "success": False,
            "error": "Session ID and total_intervals required"
        }), 400

    conn = sqlite3.connect(
    r"C:\Users\PABITRA KUMAR BARIK\OneDrive\SmartAttend AI 1\attendance.db"
)

    cursor = conn.cursor()

    end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Close session
    cursor.execute("""
        UPDATE class_sessions
        SET end_time = ?, status = ?
        WHERE id = ?
    """, (end_time, "closed", session_id))

    # Get presence scores
    cursor.execute("""
        SELECT student_id, points
        FROM presence_scores
        WHERE session_id = ?
    """, (session_id,))

    records = cursor.fetchall()

    attendance_rows = []

    for student_id, points in records:
        percentage = (points / total_intervals) * 100 if total_intervals > 0 else 0

        if percentage >= 65:
            status = "Present"
        elif percentage >= 30:
            status = "Late"
        else:
            status = "Absent"

        # Insert attendance result
        cursor.execute("""
            INSERT INTO attendance (student_id, session_id, status)
            VALUES (?, ?, ?)
        """, (student_id, session_id, status))

        # Get student info for CSV
        cursor.execute("""
            SELECT name, roll FROM students WHERE id = ?
        """, (student_id,))
        student_info = cursor.fetchone()

        today_date = datetime.now().strftime("%Y-%m-%d")

        if student_info:
            attendance_rows.append([
                today_date,
                student_info[0],
                student_info[1],
                status
            ])

    conn.commit()
    conn.close()

    # Export CSV
    filename = f"attendance_session_{session_id}.csv"

    with open(filename, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Date", "Name", "Roll", "Status"])
        writer.writerows(attendance_rows)

    return jsonify({
        "success": True,
        "message": "Session ended and attendance finalized",
        "csv_file": filename
    })




# --------------------------------------------------
# DEBUG ATTENDANCE
# --------------------------------------------------
@academic_bp.route("/debug/attendance/<int:session_id>")
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
