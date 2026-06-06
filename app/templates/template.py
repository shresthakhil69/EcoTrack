# app/__init__.py or main app file
from flask import Flask, render_template
from app.database import Database
import config

app = Flask(__name__)
app.secret_key = config.SECRET_KEY

# Initialize database
db = Database()

# Import and register blueprints
from app.routes.auth_route import auth_bp
from app.routes.home_route import home_bp  # Your existing routes

app.register_blueprint(auth_bp)
app.register_blueprint(home_bp)

# Routes for serving HTML pages
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
    # Check if user is logged in by verifying token
    # Add middleware to check JWT token
    return render_template('user/dashboard.html')

if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=5000)