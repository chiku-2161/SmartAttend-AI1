from dev2_demo import start_recognition, register_face
from smart_attendance_system.services.attendance_engine import classify_attendance


def register_student():
    register_face()
    return "✅ Student registered successfully."


def start_attendance_session():
    name = start_recognition()

    if name:
        classify_attendance(name)
        return f"✅ Attendance processed for: {name}"
    else:
        return "❌ No face recognized."
