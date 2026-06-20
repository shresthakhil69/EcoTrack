from flask import Flask


def test_help_support_saves_feedback(monkeypatch):
    from tests.conftest import register_dummy_endpoints
    from app.routes import helproute

    saved = {}

    class FakeFeedback:
        def __init__(self, user_id=None, subject=None, message=None):
            saved["user_id"] = user_id
            saved["subject"] = subject
            saved["message"] = message

        def save(self):
            saved["saved"] = True

        def get_user_feedback(self, user_id):
            return []

    monkeypatch.setattr(helproute, "Feedback", FakeFeedback)

    app = Flask(__name__)
    app.config.update(TESTING=True, SECRET_KEY="test")
    register_dummy_endpoints(app, skip_names={"help_support"})
    app.register_blueprint(helproute.helpBP)
    client = app.test_client()
    with client.session_transaction() as sess:
        sess["user_id"] = 2

    response = client.post(
        "/help_support",
        data={"subject": "Cannot submit", "message": "Image upload problem"},
    )

    assert response.status_code == 302
    assert saved == {
        "user_id": 2,
        "subject": "Cannot submit",
        "message": "Image upload problem",
        "saved": True,
    }


def test_setting_profile_rejects_invalid_phone(monkeypatch):
    from tests.conftest import register_dummy_endpoints
    from app.routes import setting_routes

    class FakeUser:
        def get_by_id(self, user_id):
            return {"id": user_id, "name": "Student", "email": "student@example.com"}

        def get_by_email(self, email):
            return None

    monkeypatch.setattr(setting_routes, "User", FakeUser)

    app = Flask(__name__)
    app.config.update(TESTING=True, SECRET_KEY="test")
    register_dummy_endpoints(app, skip_names={"setting"})
    app.register_blueprint(setting_routes.settingBP)
    client = app.test_client()
    with client.session_transaction() as sess:
        sess["user_id"] = 1

    response = client.post(
        "/setting",
        data={
            "form_type": "profile",
            "name": "Student",
            "email": "student@example.com",
            "phone": "12345",
        },
    )

    assert response.status_code == 302
    assert "/setting" in response.headers["Location"]


def test_setting_appearance_saves_dark_mode_in_session(monkeypatch):
    from tests.conftest import register_dummy_endpoints
    from app.routes import setting_routes

    class FakeUser:
        def get_by_id(self, user_id):
            return {"id": user_id, "name": "Student", "email": "student@example.com"}

    monkeypatch.setattr(setting_routes, "User", FakeUser)

    app = Flask(__name__)
    app.config.update(TESTING=True, SECRET_KEY="test")
    register_dummy_endpoints(app, skip_names={"setting"})
    app.register_blueprint(setting_routes.settingBP)
    client = app.test_client()
    with client.session_transaction() as sess:
        sess["user_id"] = 1

    response = client.post("/setting", data={"form_type": "appearance", "dark_mode": "on"})

    assert response.status_code == 302
    with client.session_transaction() as sess:
        assert sess["dark_mode"] == 1
