from app.model.database import Database
from werkzeug.security import generate_password_hash, check_password_hash


class User:

    def __init__(self, name=None, email=None, password=None, role="user"):
        self.name = name
        self.email = email
        self.password = password
        self.role = role

    # -------------------------
    # REGISTER USER
    # -------------------------
    def create_user(self):
        db = Database()

        hashed_password = generate_password_hash(self.password)

        db.execute(
            """
            INSERT INTO users (name, email, password, role)
            VALUES (%s, %s, %s, %s)
            """,
            (self.name, self.email, hashed_password, self.role)
        )

        db.close()

    # -------------------------
    # FIND USER BY EMAIL (LOGIN)
    # -------------------------
    def get_by_email(self, email):
        db = Database()

        user = db.fetch_one(
            "SELECT * FROM users WHERE email=%s",
            (email,)
        )

        db.close()
        return user

    # -------------------------
    # CHECK PASSWORD
    # -------------------------
    def check_password(self, hashed_password, plain_password):
        return check_password_hash(hashed_password, plain_password)

    # -------------------------
    # GET USER BY ID
    # -------------------------
    def get_by_id(self, user_id):
        db = Database()

        user = db.fetch_one(
            "SELECT * FROM users WHERE id=%s",
            (user_id,)
        )

        db.close()
        return user

    # -------------------------
    # UPDATE PROFILE
    # -------------------------
    def update_profile(self, user_id, name, email):
        db = Database()
        db.execute(
            """
            UPDATE users SET name=%s, email=%s
            WHERE id=%s
            """,
            (name, email, user_id)
        )
        db.close()

    # -------------------------
    # UPDATE PASSWORD
    # -------------------------
    def update_password(self, user_id, new_password):
        db = Database()
        hashed = generate_password_hash(new_password)
        db.execute(
            """
            UPDATE users SET password=%s
            WHERE id=%s
            """,
            (hashed, user_id)
        )
        db.close()

    # -------------------------
    # DELETE USER ACCOUNT
    # -------------------------
    def delete_account(self, user_id):
        db = Database()
        db.execute("DELETE FROM users WHERE id=%s", (user_id,))
        db.close()
