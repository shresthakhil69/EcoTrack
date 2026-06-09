from flask import Flask, render_template, session, redirect, url_for
from app.models.database import Database
import config

app = Flask(__name__)
app.secret_key = config.SECRET_KEY

# Database object
db = Database()

# Register blueprints
from app.routes.auth_route import auth_bp
from app.routes.report_route import report
from app.routes.my_report_route import my_report

app.register_blueprint(auth_bp)
app.register_blueprint(report)
app.register_blueprint(my_report)

# Register admin blueprint safely
try:
    from app.routes.admin_auth_route import admin_bp
    app.register_blueprint(admin_bp)
except Exception:
    pass


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/register")
def register_page():
    return render_template("auth/register.html")


@app.route("/login")
def login_page():
    return render_template("auth/login.html")


@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect(url_for("login_page"))

    summary = {
        "total": 0,
        "pending": 0,
        "resolved": 0
    }

    recent_reports = []

    return render_template(
        "user/dashboard.html",
        summary=summary,
        recent_reports=recent_reports
    )


@app.route("/settings")
def settings():
    if "user_id" not in session:
        return redirect(url_for("login_page"))

    return render_template("user/setting.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login_page"))
