import sqlite3

SESSION_DURATION_MINUTES = 45
SAMPLING_INTERVAL_SECONDS = 30


def calculate_total_samples():
    return int((SESSION_DURATION_MINUTES * 60) / SAMPLING_INTERVAL_SECONDS)


def classify_attendance(points):
    total_samples = calculate_total_samples()

    if points >= 0.75 * total_samples:
        return "Present"
    elif points >= 0.40 * total_samples:
        return "Late"
    else:
        return "Absent"


def finalize_session(session_id):
    conn = sqlite3.connect(
    r"C:\Users\PABITRA KUMAR BARIK\OneDrive\SmartAttend AI 1\attendance.db"
)

    cursor = conn.cursor()

    # Get students belonging to the section of this session
    cursor.execute("""
        SELECT students.id
        FROM students
        JOIN subject_assignments sa ON students.section_id = sa.section_id
        JOIN class_sessions cs ON cs.subject_assignment_id = sa.id
        WHERE cs.id = ?
    """, (session_id,))

    students = cursor.fetchall()

    for student in students:
        student_id = student[0]

        cursor.execute("""
            SELECT points FROM presence_scores
            WHERE student_id = ? AND session_id = ?
        """, (student_id, session_id))

        result = cursor.fetchone()
        points = result[0] if result else 0

        status = classify_attendance(points)

        cursor.execute("""
            INSERT INTO attendance (student_id, session_id, status)
            VALUES (?, ?, ?)
        """, (student_id, session_id, status))

    # Mark session as ended
    cursor.execute("""
        UPDATE class_sessions
        SET status = 'ended'
        WHERE id = ?
    """, (session_id,))

    conn.commit()
    conn.close()
