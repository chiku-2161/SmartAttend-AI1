import cv2
import sqlite3
import os
import time
import numpy as np
from datetime import datetime

FACE_DIR = "faces"
SESSION_ID = 1
CHECK_INTERVAL = 3

os.makedirs(FACE_DIR, exist_ok=True)


# ---------- DATABASE ----------
def get_db():
    return sqlite3.connect(
    r"C:\Users\PABITRA KUMAR BARIK\OneDrive\SmartAttend AI 1\attendance.db"
)



def update_presence(student_id):
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        SELECT id, points FROM presence_scores
        WHERE student_id=? AND session_id=?
    """, (student_id, SESSION_ID))

    row = cur.fetchone()

    if row:
        cur.execute("""
            UPDATE presence_scores
            SET points = points + 1
            WHERE id = ?
        """, (row[0],))
    else:
        cur.execute("""
            INSERT INTO presence_scores (student_id, session_id, points)
            VALUES (?, ?, 1)
        """, (student_id, SESSION_ID))

    conn.commit()
    conn.close()



# ---------- REGISTER FACE ----------
def register_face():
    name = input("Enter student name: ")
    roll = input("Enter roll number: ")

    cap = cv2.VideoCapture(0)
    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    )

    print("Press S to capture face")

    while True:
        ret, frame = cap.read()
        frame = cv2.flip(frame, 1)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

        cv2.imshow("Register", frame)

        if cv2.waitKey(1) & 0xFF == ord("s") and len(faces) == 1:
            (x, y, w, h) = faces[0]
            face_img = gray[y:y+h, x:x+w]
            face_img = cv2.resize(face_img, (200, 200))
            break

    cap.release()
    cv2.destroyAllWindows()

    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
    INSERT INTO students (name, roll, section_id)
    VALUES (?, ?, ?)
""", (name, roll, 1))


    student_id = cur.lastrowid
    conn.commit()
    conn.close()

    cv2.imwrite(f"{FACE_DIR}/{student_id}.jpg", face_img)
    print(f"✅ Face saved for {name} (ID={student_id})")


# ---------- TRAIN MODEL ----------3
def train_model():
    faces = []
    labels = []

    for file in os.listdir(FACE_DIR):
        if file.endswith(".jpg"):
            img = cv2.imread(f"{FACE_DIR}/{file}", cv2.IMREAD_GRAYSCALE)
            faces.append(img)
            labels.append(int(file.split(".")[0]))

    if len(faces) == 0:
        print("❌ No registered faces found.")
        return None

    model = cv2.face.LBPHFaceRecognizer_create()
    model.train(faces, np.array(labels))
    return model


def reset_presence():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM presence_scores")
    conn.commit()
    conn.close()

# ---------- RECOGNITION ----------
# ---------- RECOGNITION ----------
def start_recognition():
    print("Starting recognition...")

    reset_presence()
    model = train_model()
    if model is None:
        return None   # important

    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    )

    cap = cv2.VideoCapture(0)
    last_update = time.time()

    final_recognized_id = None   # ⭐ store last recognized student

    while True:
        ret, frame = cap.read()
        frame = cv2.flip(frame, 1)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        recognized = set()

        for (x, y, w, h) in faces:
            face_img = gray[y:y+h, x:x+w]
            face_img = cv2.resize(face_img, (200, 200))

            label, confidence = model.predict(face_img)

            if confidence < 80:
                recognized.add(label)
                final_recognized_id = label   # ⭐ save ID
                text = f"ID {label}"
            else:
                text = "Unknown"

            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.putText(frame, text, (x, y-10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

        if time.time() - last_update > CHECK_INTERVAL:
            for sid in recognized:
                update_presence(sid)
                print(f"Presence +1 → student {sid}")
            last_update = time.time()

        cv2.imshow("Recognition", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()
    show_attendance()

    return final_recognized_id   # ⭐⭐⭐ MOST IMPORTANT


# FINAL ATTENDANCE 
def show_attendance():
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        SELECT student_id, points FROM presence_scores
        WHERE session_id=?
    """, (SESSION_ID,))

    rows = cur.fetchall()

    print("\n===== FINAL ATTENDANCE =====")

    for sid, points in rows:
        percent = min(points * 20, 100)

        if percent >= 70:
            status = "Present"
        elif percent >= 40:
            status = "Late Entry"
        else:
            status = "Absent"

        print(f"Student {sid} → {percent:.1f}% → {status}")

    conn.close()


# MENU 
def main():
    while True:
        print("\n1. Register Student Face")
        print("2. Start Recognition Session")
        print("3. Exit")

        ch = input("Enter choice: ")

        if ch == "1":
            register_face()
        elif ch == "2":
            start_recognition()
        elif ch == "3":
            break


if __name__ == "__main__":
    main()
