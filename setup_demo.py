import sqlite3

conn = sqlite3.connect(
    r"C:\Users\PABITRA KUMAR BARIK\OneDrive\SmartAttend AI 1\attendance.db"
)

cursor = conn.cursor()

# Teacher
cursor.execute("""
INSERT OR IGNORE INTO teachers (id, name, email, password)
VALUES (1, 'Demo Teacher', 'demo@mail.com', '1234')
""")

# Section
cursor.execute("""
INSERT OR IGNORE INTO sections (id, name, department, year)
VALUES (1, 'CSE-A', 'CSE', '2')
""")

# Subject
cursor.execute("""
INSERT OR IGNORE INTO subjects (id, name, code)
VALUES (1, 'AI', 'AI101')
""")

# Assignment
cursor.execute("""
INSERT OR IGNORE INTO subject_assignments (id, teacher_id, subject_id, section_id)
VALUES (1, 1, 1, 1)
""")

conn.commit()
conn.close()

print("✅ Demo data inserted successfully!")
