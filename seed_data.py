import sqlite3

conn = sqlite3.connect("attendance.db")
cursor = conn.cursor()

# Insert Section
cursor.execute("""
INSERT INTO sections (name, department, year)
VALUES ('CSE-A', 'CSE', 2)
""")

# Insert Student
cursor.execute("""
INSERT INTO students (name, roll, section_id)
VALUES ('John Doe', '101', 1)
""")

# Insert Teacher
cursor.execute("""
INSERT INTO teachers (name, email, password)
VALUES ('Mr Smith', 'smith@test.com', '1234')
""")

# Insert Subject
cursor.execute("""
INSERT INTO subjects (name, code)
VALUES ('Data Structures', 'CS201')
""")

# Insert Subject Assignment
cursor.execute("""
INSERT INTO subject_assignments (teacher_id, subject_id, section_id)
VALUES (1, 1, 1)
""")

conn.commit()
conn.close()

print("Seed data inserted successfully.")
