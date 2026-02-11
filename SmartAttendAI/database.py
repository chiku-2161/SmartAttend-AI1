import sqlite3

def init_db():
    conn = sqlite3.connect("attendance.db")
    cursor = conn.cursor()

    # Sections
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS sections (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        department TEXT,
        year INTEGER
    )
    """)

    # Students
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        roll TEXT UNIQUE NOT NULL,
        section_id INTEGER,
        embedding TEXT,
        FOREIGN KEY(section_id) REFERENCES sections(id)
    )
    """)

    # Teachers
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS teachers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
    """)

    # Subjects
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS subjects (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        code TEXT UNIQUE NOT NULL
    )
    """)

    # Subject Assignments
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS subject_assignments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        teacher_id INTEGER,
        subject_id INTEGER,
        section_id INTEGER,
        FOREIGN KEY(teacher_id) REFERENCES teachers(id),
        FOREIGN KEY(subject_id) REFERENCES subjects(id),
        FOREIGN KEY(section_id) REFERENCES sections(id)
    )
    """)

    # Class Sessions
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS class_sessions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        subject_assignment_id INTEGER,
        start_time TEXT,
        end_time TEXT,
        status TEXT,
        FOREIGN KEY(subject_assignment_id) REFERENCES subject_assignments(id)
    )
    """)

    # Presence Scores
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS presence_scores (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER,
        session_id INTEGER,
        points INTEGER DEFAULT 0,
        FOREIGN KEY(student_id) REFERENCES students(id),
        FOREIGN KEY(session_id) REFERENCES class_sessions(id)
    )
    """)

    # Final Attendance
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS attendance (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER,
        session_id INTEGER,
        status TEXT,
        FOREIGN KEY(student_id) REFERENCES students(id),
        FOREIGN KEY(session_id) REFERENCES class_sessions(id)
    )
    """)

    conn.commit()
    conn.close()
