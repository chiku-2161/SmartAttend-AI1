from flask import Flask

# Correct relative imports (same package se)
from .database import init_db
from .routes.session_routes import session_bp
from .routes.analytics_routes import analytics_bp
from .routes.academic_routes import academic_bp


app = Flask(__name__)

# Initialize database
init_db()

# Register blueprints
app.register_blueprint(session_bp)
app.register_blueprint(analytics_bp)
app.register_blueprint(academic_bp)


@app.route("/")
def home():
    return {
        "success": True,
        "data": {},
        "message": "Smart Attendance System Running"
    }


if __name__ == "__main__":
    app.run(debug=True)
