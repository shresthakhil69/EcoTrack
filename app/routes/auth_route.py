from flask import Blueprint, request, jsonify,session
import jwt
from datetime import datetime, timedelta
import config
from app.models.database import Database
from app.models.user import User

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

# Initialize database connection
db = Database()
user_model = User(db)

@auth_bp.route('/register', methods=['POST'])
def register():
    """
    Register a new user
    Expected JSON: {
        "username": "user123",
        "email": "user@example.com",
        "password": "securepass123",
        "fullname": "User Name"
    }
    """
    try:
        data = request.get_json()
        
        # Check if all required fields are present
        required_fields = ['username', 'email', 'password', 'fullname']
        if not all(key in data for key in required_fields):
            return jsonify({"success": False, "message": "Missing required fields"}), 400
        
        username = data.get('username', '').strip()
        email = data.get('email', '').strip()
        password = data.get('password', '').strip()
        fullname = data.get('fullname', '').strip()
        
        # Validate input
        if len(username) < 3:
            return jsonify({"success": False, "message": "Username must be at least 3 characters"}), 400
        if len(password) < 6:
            return jsonify({"success": False, "message": "Password must be at least 6 characters"}), 400
        if '@' not in email:
            return jsonify({"success": False, "message": "Invalid email format"}), 400
        
        # Register user
        result = user_model.register_user(username, email, password, fullname)
        
        if result['success']:
            return jsonify(result), 201
        else:
            return jsonify(result), 400
            
    except Exception as e:
        return jsonify({"success": False, "message": f"Server error: {str(e)}"}), 500


@auth_bp.route('/login', methods=['POST'])
def login():
    """
    Login user and return JWT token
    Expected JSON: {
        "username": "user123",
        "password": "securepass123"
    }
    """
    try:
        data = request.get_json()
        
        username = data.get('username', '').strip()
        password = data.get('password', '').strip()
        
        if not username or not password:
            return jsonify({"success": False, "message": "Username and password required"}), 400
        
        # Login user
        result = user_model.login_user(username, password)
        
        if result['success']:
            # Generate JWT token
            session["user_id"] = result["user_id"]
            session["username"] = result["username"]
            session["fullname"] = result.get("fullname")
            
            token = jwt.encode({
                'user_id': result['user_id'],
                'username': result['username'],
                'email': result['email'],
                'exp': datetime.utcnow() + timedelta(hours=24)
            }, config.SECRET_KEY, algorithm='HS256')
            
            return jsonify({
                "success": True,
                "message": "Login successful!",
                "token": token,
                "user": {
                    "user_id": result['user_id'],
                    "username": result['username'],
                    "email": result['email'],
                    "fullname": result['fullname']
                }
            }), 200
        else:
            return jsonify(result), 401
            
    except Exception as e:
        return jsonify({"success": False, "message": f"Server error: {str(e)}"}), 500


@auth_bp.route('/verify-token', methods=['POST'])
def verify_token():
    """
    Verify JWT token
    Expected Header: Authorization: Bearer <token>
    """
    try:
        token = request.headers.get('Authorization', '').replace('Bearer ', '')
        
        if not token:
            return jsonify({"success": False, "message": "Token missing"}), 401
        
        decoded = jwt.decode(token, config.SECRET_KEY, algorithms=['HS256'])
        return jsonify({
            "success": True,
            "message": "Token valid",
            "user": decoded
        }), 200
        
    except jwt.ExpiredSignatureError:
        return jsonify({"success": False, "message": "Token expired"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"success": False, "message": "Invalid token"}), 401
    except Exception as e:
        return jsonify({"success": False, "message": f"Server error: {str(e)}"}), 500