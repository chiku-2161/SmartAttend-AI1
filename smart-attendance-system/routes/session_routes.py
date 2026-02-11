from flask import Blueprint, request, jsonify
from datetime import datetime
import sqlite3
from services.attendance_engine import finalize_session

session_bp = Blueprint("session_bp", __name__)


@session_bp.route("/session/start", methods=["POST"])
def start_session():
    data = request.get_json()
    subject_assignment_id = data.get("subject_assignment_id")

    if not subject_assignment_id:
        return jsonify({
            "success": False,
            "error": "subject_assignment_id is required"
        })

    conn = sqlite3.connect("attendance.db")
    cursor = conn.cursor()

    start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute("""
        INSERT INTO class_sessions (subject_assignment_id, start_time, status)
        VALUES (?, ?, 'active')
    """, (subject_assignment_id, start_time))

    session_id = cursor.lastrowid
    conn.commit()
    conn.close()

    return jsonify({
        "success": True,
        "data": {"session_id": session_id},
        "message": "Session started"
    })


@session_bp.route("/session/end", methods=["POST"])
def end_session():
    data = request.get_json()
    session_id = data.get("session_id")

    if not session_id:
        return jsonify({
            "success": False,
            "error": "session_id is required"
        })

    finalize_session(session_id)

    end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    conn = sqlite3.connect("attendance.db")
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE class_sessions
        SET end_time = ?
        WHERE id = ?
    """, (end_time, session_id))

    conn.commit()
    conn.close()

    return jsonify({
        "success": True,
        "data": {},
        "message": "Session finalized successfully"
    })
