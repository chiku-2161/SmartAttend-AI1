from flask import Flask

# Correct absolute package imports
from smart_attendance_system.database import init_db
from smart_attendance_system.routes.student_routes import student_bp
from smart_attendance_system.routes.attendance_routes import attendance_bp
from smart_attendance_system.routes.teacher_routes import teacher_bp
from smart_attendance_system.routes.academic_routes import academic_bp


app = Flask(__name__)

# Initialize DB
init_db()

# Register all blueprints
app.register_blueprint(student_bp)
app.register_blueprint(attendance_bp)
app.register_blueprint(teacher_bp)
app.register_blueprint(academic_bp)


@app.route("/")
def home():
    return {"message": "Smart Integrity System Running"}


if __name__ == "__main__":
    app.run(debug=True)

