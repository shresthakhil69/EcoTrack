from werkzeug.security import generate_password_hash


def test_register_controller_rejects_password_mismatch(app, monkeypatch):
    from app.controller import user_login_controller

    class FakeUser:
        pass

    monkeypatch.setattr(user_login_controller, "User", FakeUser)

    with app.test_request_context(
        "/register",
        method="POST",
        data={
            "name": "Student",
            "email": "student@example.com",
            "password": "secret123",
            "confirm_password": "different123",
        },
    ):
        response = user_login_controller.register_controller()

    assert response.status_code == 302
    assert "/register" in response.headers["Location"]


def test_register_controller_creates_new_user(app, monkeypatch):
    from app.controller import user_login_controller

    created = {}

    class FakeUser:
        def __init__(self, name=None, email=None, password=None, role="user"):
            self.name = name
            self.email = email
            self.password = password
            self.role = role

        def get_by_email(self, email):
            return None

        def create_user(self):
            created["name"] = self.name
            created["email"] = self.email
            created["password"] = self.password
            created["role"] = self.role

    monkeypatch.setattr(user_login_controller, "User", FakeUser)

    with app.test_request_context(
        "/register",
        method="POST",
        data={
            "name": "Student",
            "email": "student@example.com",
            "password": "secret123",
            "confirm_password": "secret123",
        },
    ):
        response = user_login_controller.register_controller()

    assert response.status_code == 302
    assert "/login" in response.headers["Location"]
    assert created == {
        "name": "Student",
        "email": "student@example.com",
        "password": "secret123",
        "role": "user",
    }


def test_login_controller_sets_session_for_valid_user(app, monkeypatch):
    from flask import session
    from app.controller import user_login_controller

    hashed = generate_password_hash("secret123")

    class FakeUser:
        def get_by_email(self, email):
            return {
                "id": 4,
                "name": "Student",
                "email": email,
                "password": hashed,
                "role": "user",
            }

        def check_password(self, hashed_password, plain_password):
            return plain_password == "secret123"

    monkeypatch.setattr(user_login_controller, "User", FakeUser)

    with app.test_request_context(
        "/login",
        method="POST",
        data={"email": "student@example.com", "password": "secret123"},
    ):
        response = user_login_controller.login_controller()
        assert session["user_id"] == 4
        assert session["user_name"] == "Student"
        assert session["user_email"] == "student@example.com"
        assert session["user_role"] == "user"

    assert response.status_code == 302
    assert "/dashboard" in response.headers["Location"]


def test_logout_controller_clears_session(app):
    from flask import session
    from app.controller import user_login_controller

    with app.test_request_context("/logout"):
        session["user_id"] = 99
        response = user_login_controller.logout_controller()
        assert "user_id" not in session

    assert response.status_code == 302
    assert response.headers["Location"].endswith("/")
