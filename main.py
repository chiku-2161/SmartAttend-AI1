from dev2_demo import start_recognition
import requests
from dev2_demo import register_face

session_id = None   # single global session variable


def start_class():
    global session_id

    print("👨‍🏫 Starting class session...")

    data = {
        "teacher_id": 1,
        "assignment_id": 1
    }

    res = requests.post("http://127.0.0.1:5000/teacher/start-class", json=data)
    result = res.json()

    if result.get("success"):
        session_id = result["session_id"]
        print("✅ Class started. Session ID:", session_id)
    else:
        print("❌ Failed:", result.get("error"))


def scan_attendance():
    global session_id

    if not session_id:
        print("⚠️ Start class first!")
        return

    name = start_recognition()

    if not name:
        print("❌ No face recognized")
        return

    data = {
        "session_id": session_id,
        "student_id": int(name)
    }

    requests.post("http://127.0.0.1:5000/session/increment", json=data)
    print(f"📍 Presence marked for student {name}")


def end_class():
    global session_id

    if not session_id:
        print("❌ No active session.")
        return

    print("🛑 Ending class...")

    res = requests.post(
        "http://127.0.0.1:5000/session/end",
        json={
            "session_id": session_id,
            "total_intervals": 5
        }
    )

    data = res.json()

    if not data.get("success"):
        print("❌ Failed to end session.")
        return

    print("\n📊 FINAL ATTENDANCE DASHBOARD\n")

    # fetch final attendance
    debug = requests.get(
        f"http://127.0.0.1:5000/debug/attendance/{session_id}"
    )

    rows = debug.json()

    for student_id, status in rows:
        print(f"Student {student_id} → {status}")

    print("\n📄 CSV Saved:", data.get("csv_file"))

    session_id = None  # reset after end


def main():
    while True:
        print("\n====== Teacher Attendance Panel ======")
        print("1. register face")
        print("2. Start Class")
        print("3. Scan Attendance")
        print("4. End Class")
        print("5. Exit")

        choice = input("Enter choice: ")


        if choice == "1":
            register_face()
        elif choice == "2":
            start_class()
        elif choice == "3":
            scan_attendance()
        elif choice == "4":
            end_class()
        elif choice == "5":
            
            break
        else:
            print("Invalid choice")


if __name__ == "__main__":
    main()
