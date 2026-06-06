from flask import Flask, render_template
from app.database import Database
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

import config

# Create Flask app
app = Flask(__name__)
app.secret_key = config.SECRET_KEY

# Initialize database
db = Database()

# Register blueprints
from app.routes.auth_route import auth_bp
app.register_blueprint(auth_bp)

# HTML Routes
@app.route("/")
def home():
    return render_template("home.html") 

@app.route('/')
def index():
    return render_template('base.html')

@app.route('/register')
def register_page():
    return render_template('auth/register.html')

@app.route('/login')
def login_page():
    return render_template('auth/login.html')

@app.route('/dashboard')
def dashboard():
    return render_template('user/dashboard.html')
from app.routes.home_route import home
from app.routes.auth_route import auth
from app.routes.my_report_route import my_report
from app.routes.report_route import report

app.register_blueprint(home)
app.register_blueprint(auth)
app.register_blueprint(my_report)
app.register_blueprint(report)




