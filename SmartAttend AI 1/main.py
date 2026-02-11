from dev2_demo import start_recognition
from dev2_demo import register_face
from smart_attendance_system.services.attendance_engine import classify_attendance


def main():
    while True:
        print("\n========== SmartAttend AI ==========")
        print("1. Register Student Face")
        print("2. Start Attendance Session")
        print("3. View Attendance Risk")
        print("4. Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            register_face()

        elif choice == "2":
            print("\n📸 Starting recognition...")
            name = start_recognition()

            if name:
                classify_attendance(name)
                print(f"\n✅ Attendance processed for: {name}")
            else:
                print("\n❌ No face recognized.")

        elif choice == "3":
            from smart_attendance_system.services.analytics_engine import show_risk
            show_risk()

        elif choice == "4":
            print("Exiting SmartAttend AI...")
            break

        else:
            print("Invalid choice. Try again.")


if __name__ == "__main__":
    main()
