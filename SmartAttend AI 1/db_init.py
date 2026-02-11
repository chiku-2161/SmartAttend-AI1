import sqlite3

conn = sqlite3.connect("attendance.db")
cur = conn.cursor()

cur.execute("DELETE FROM students")
cur.execute("DELETE FROM presence_scores")

conn.commit()
conn.close()

print("DB reset done")
