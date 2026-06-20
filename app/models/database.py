import pymysql
import config

class Database:
    def __init__(self):
        """Open a database connection when object is created."""
        try:
            self.__connection = pymysql.connect(
                host=config.MYSQL_HOST,
                user=config.MYSQL_USER,
                password=config.MYSQL_PASSWORD,
                database=config.MYSQL_DATABASE,
                cursorclass=pymysql.cursors.DictCursor,
            )
            print("Database connected successfully!")
        except pymysql.MySQLError as e:
            print("Database connection failed!")
            print("Error:", e)
 
    def fetch_one(self, query, params=None):
        """Run a query and return ONE result (or None)."""
        cursor = self.__connection.cursor(pymysql.cursors.DictCursor)
        cursor.execute(query, params)
        result = cursor.fetchone()
        cursor.close()
        return result

    def fetch_all(self, query, params=None):
        cursor = self.__connection.cursor(pymysql.cursors.DictCursor)
        cursor.execute(query, params)
        result = cursor.fetchall()
        cursor.close()
        return result

    def execute(self, query, params=None):
        """Run a query that changes data (INSERT, UPDATE, DELETE)."""
        cursor = self.__connection.cursor()
        cursor.execute(query, params)
        self.__connection.commit()
        cursor.close()

    def close(self):
        """Close the database connection."""
        self.__connection.close()

                        
    # ── Static Method: Create tables on app startup ─────────

    @staticmethod
    def create_tables():
        """
        Create database tables if they don't exist.

        @staticmethod: belongs to the class but doesn't need
        'self' — it doesn't use any instance data.
        You call it as: Database.create_tables()
        """
        db = Database()
        db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                email VARCHAR(100) NOT NULL UNIQUE,
                password VARCHAR(255) NOT NULL,
                role VARCHAR(20) NOT NULL DEFAULT 'user',
                reported_on TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        db.execute("""
            CREATE TABLE IF NOT EXISTS reports (
                id INT AUTO_INCREMENT PRIMARY KEY,

                user_id INT NOT NULL,

                waste_type VARCHAR(255),
                description TEXT,

                location VARCHAR(255),

                image_path VARCHAR(255),

                status ENUM(
                    'pending',
                    'in_progress',
                    'resolved'
                ) DEFAULT 'pending',

                reported_on TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

                FOREIGN KEY (user_id)
                REFERENCES users(id)
            )
        """)
        db.execute("""
            CREATE TABLE IF NOT EXISTS notifications (
                id INT AUTO_INCREMENT PRIMARY KEY,

                user_id INT NOT NULL,

                report_id INT NOT NULL,

                message TEXT,

                is_read BOOLEAN DEFAULT FALSE,

                reported_on TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

                FOREIGN KEY (user_id)
                REFERENCES users(id),

                FOREIGN KEY (report_id)
                REFERENCES reports(id)
            )
        """)
        db.execute("""
            CREATE TABLE IF NOT EXISTS reports (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL,
                waste_type VARCHAR(255),
                description TEXT,
                location VARCHAR(255),
                image_path VARCHAR(255),
                status ENUM('pending', 'in_progress', 'resolved') DEFAULT 'pending',
                reported_on TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        """)
        
        # Create default admin if not exists
        admin = db.fetch_one(
            "SELECT * FROM users WHERE email = %s", ("admin@admin.com",)
        )
        if not admin:
            from werkzeug.security import generate_password_hash

            db.execute(
                "INSERT INTO users (name, email, password, role) VALUES (%s, %s, %s, %s)",
                ("Admin", "admin@admin.com", generate_password_hash("admin123"), "admin"),
            )

        db.close()
