from flask import Flask


class FakeDatabaseForAdmin:
    instances = []

    def __init__(self):
        self.executed = []
        FakeDatabaseForAdmin.instances.append(self)

    def fetch_one(self, query, params=None):
        return {"total": 3}

    def fetch_all(self, query, params=None):
        return []

    def execute(self, query, params=None):
        self.executed.append((" ".join(query.split()), params))

    def close(self):
        pass


def make_admin_app(monkeypatch):
    from tests.conftest import register_dummy_endpoints
    from app.routes import admindashboardroute

    flask_app = Flask(__name__)
    flask_app.config.update(TESTING=True, SECRET_KEY="test")
    register_dummy_endpoints(flask_app, skip_names={"admin_dashboard"})
    flask_app.register_blueprint(admindashboardroute.admin_dashboardBP)
    return flask_app, admindashboardroute


def test_admin_dashboard_requires_admin_login(monkeypatch):
    app, _ = make_admin_app(monkeypatch)
    client = app.test_client()

    response = client.get("/admin/dashboard")

    assert response.status_code == 302
    assert "/admin_login" in response.headers["Location"]


def test_admin_update_status_updates_report_and_creates_notification(monkeypatch):
    app, route_module = make_admin_app(monkeypatch)

    calls = {}

    class FakeReport:
        def find_by_id(self, report_id):
            calls["find_by_id"] = report_id
            return {"id": int(report_id), "user_id": 7, "status": "pending"}

        def update_status(self, report_id, status):
            calls["update_status"] = (report_id, status)

    def fake_create_notification(user_id, report_id, new_status):
        calls["notification"] = (user_id, report_id, new_status)

    monkeypatch.setattr(route_module, "Report", FakeReport)

    # The route imports create_notification inside the function, so patch that module.
    from app.controller import notification_controller

    monkeypatch.setattr(notification_controller, "create_notification", fake_create_notification)

    client = app.test_client()
    with client.session_transaction() as sess:
        sess["admin_id"] = 1

    response = client.post("/admin/update_status", data={"report_id": "3", "status": "resolved"})

    assert response.status_code == 302
    assert calls["find_by_id"] == "3"
    assert calls["update_status"] == ("3", "resolved")
    assert calls["notification"] == (7, "3", "resolved")


def test_admin_rejects_invalid_report_status(monkeypatch):
    app, _ = make_admin_app(monkeypatch)
    client = app.test_client()
    with client.session_transaction() as sess:
        sess["admin_id"] = 1

    response = client.post("/admin/update_status", data={"report_id": "3", "status": "wrong"})

    assert response.status_code == 302
    assert "/admin/dashboard" in response.headers["Location"]


def test_admin_update_feedback_rejects_invalid_status(monkeypatch):
    app, _ = make_admin_app(monkeypatch)
    client = app.test_client()
    with client.session_transaction() as sess:
        sess["admin_id"] = 1

    response = client.post(
        "/admin/feedback/update_status",
        data={"feedback_id": "4", "status": "invalid"},
    )

    assert response.status_code == 302
    assert "/admin/feedback" in response.headers["Location"]
