import bcrypt
from datetime import datetime

class User:
    def __init__(self, database):
        self.db = database
        self.create_table()
    
    def create_table(self):
        """Create users table if it doesn't exist"""
        cursor = self.db.get_cursor()
        try:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    username VARCHAR(50) UNIQUE NOT NULL,
                    email VARCHAR(100) UNIQUE NOT NULL,
                    password VARCHAR(255) NOT NULL,
                    fullname VARCHAR(100),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            self.db.commit()
            print("Users table created/verified successfully!")
        except Exception as e:
            print(f"Error creating users table: {e}")
    
    def hash_password(self, password):
        """Hash password using bcrypt"""
        salt = bcrypt.gensalt(rounds=10)
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')
    
    def verify_password(self, password, hashed_password):
        """Verify password against hash"""
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))
    
    def register_user(self, username, email, password, fullname):
        """Register a new user"""
        cursor = self.db.get_cursor()
        try:
            # Check if user already exists
            cursor.execute("SELECT * FROM users WHERE username = %s OR email = %s", (username, email))
            if cursor.fetchone():
                return {"success": False, "message": "Username or email already exists"}
            
            # Hash password and insert user
            hashed_password = self.hash_password(password)
            cursor.execute(
                "INSERT INTO users (username, email, password, fullname) VALUES (%s, %s, %s, %s)",
                (username, email, hashed_password, fullname)
            )
            self.db.commit()
            return {"success": True, "message": "User registered successfully!"}
        except Exception as e:
            return {"success": False, "message": f"Registration error: {str(e)}"}
    
    def login_user(self, username, password):
        """Login user and return user data if credentials match"""
        cursor = self.db.get_cursor()
        try:
            cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
            user = cursor.fetchone()
            
            if not user:
                return {"success": False, "message": "User not found"}
            
            if self.verify_password(password, user['password']):
                return {
                    "success": True,
                    "message": "Login successful!",
                    "user_id": user['id'],
                    "username": user['username'],
                    "email": user['email'],
                    "fullname": user['fullname']
                }
            else:
                return {"success": False, "message": "Invalid password"}
        except Exception as e:
            return {"success": False, "message": f"Login error: {str(e)}"}
    
    def get_user_by_id(self, user_id):
        """Get user by ID"""
        cursor = self.db.get_cursor()
        try:
            cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
            return cursor.fetchone()
        except Exception as e:
            print(f"Error fetching user: {e}")
            return None