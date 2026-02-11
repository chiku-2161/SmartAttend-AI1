import sqlite3

conn = sqlite3.connect("attendance.db")
cursor = conn.cursor()

# Insert fake attendance records
records = [
    (1, 1, 'Present'),
    (1, 2, 'Present'),
    (1, 3, 'Absent'),
    (1, 4, 'Present'),
    (1, 5, 'Late'),
]

for record in records:
    cursor.execute("""
        INSERT INTO attendance (student_id, session_id, status)
        VALUES (?, ?, ?)
    """, record)

conn.commit()
conn.close()

print("Dummy attendance inserted.")
