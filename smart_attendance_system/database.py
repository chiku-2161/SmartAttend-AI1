import sqlite3


def init_db():
    conn = sqlite3.connect(
        r"C:\Users\PABITRA KUMAR BARIK\OneDrive\SmartAttend AI 1\attendance.db"
    )
    cursor = conn.cursor()

    # ---------------- TABLES ---------------- #

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS sections (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        department TEXT,
        year INTEGER
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        roll TEXT UNIQUE NOT NULL,
        section_id INTEGER,
        FOREIGN KEY(section_id) REFERENCES sections(id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS teachers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS subjects (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        code TEXT UNIQUE NOT NULL
    )
    """)

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

    # ---------------- DEMO DATA ---------------- #

    # Section
    cursor.execute("SELECT COUNT(*) FROM sections")
    if cursor.fetchone()[0] == 0:
        cursor.execute(
            "INSERT INTO sections (name, department, year) VALUES ('CSE-A', 'CSE', 3)"
        )

    # Teacher
    cursor.execute("SELECT COUNT(*) FROM teachers")
    if cursor.fetchone()[0] == 0:
        cursor.execute(
            "INSERT INTO teachers (name, email, password) VALUES ('Dr. AI', 'ai@college.com', '1234')"
        )

    # Subject
    cursor.execute("SELECT COUNT(*) FROM subjects")
    if cursor.fetchone()[0] == 0:
        cursor.execute(
            "INSERT INTO subjects (name, code) VALUES ('Artificial Intelligence', 'AI101')"
        )

    # Subject Assignment
    cursor.execute("SELECT COUNT(*) FROM subject_assignments")
    if cursor.fetchone()[0] == 0:
        cursor.execute("""
        INSERT INTO subject_assignments (teacher_id, subject_id, section_id)
        VALUES (1, 1, 1)
        """)

    conn.commit()
    conn.close()
