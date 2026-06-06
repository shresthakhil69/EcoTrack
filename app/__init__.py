from flask import Flask, render_template
from app.database import Database
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