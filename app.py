from flask import Flask
from database import init_db
from routes.session_routes import session_bp
from routes.analytics_routes import analytics_bp

app = Flask(__name__)

init_db()

app.register_blueprint(session_bp)
app.register_blueprint(analytics_bp)

@app.route("/")
def home():
    return {
        "success": True,
        "data": {},
        "message": "Smart Attendance System Running"
    }

if __name__ == "__main__":
    app.run(debug=True)
