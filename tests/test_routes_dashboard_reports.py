from flask import Flask


def test_dashboard_redirects_guest_to_login(monkeypatch):
    from app.routes import dashboardroute

    app = Flask(__name__)
    app.config.update(TESTING=True, SECRET_KEY="test")

    from tests.conftest import register_dummy_endpoints

    register_dummy_endpoints(app, skip_names={"dashboard"})
    app.register_blueprint(dashboardroute.dashboardBP)
    client = app.test_client()

    response = client.get("/dashboard")

    assert response.status_code == 302
    assert "/login" in response.headers["Location"]


def test_dashboard_summary_counts_user_reports(monkeypatch):
    from app.routes import dashboardroute

    captured = {}

    class FakeReport:
        def get_user_reports(self, user_id):
            assert user_id == 1
            return [
                {"id": 1, "status": "pending"},
                {"id": 2, "status": "in_progress"},
                {"id": 3, "status": "resolved"},
                {"id": 4, "status": "resolved"},
            ]

        def search_user_reports(self, user_id, search_query):
            return []

    def fake_render_template(template, **context):
        captured["template"] = template
        captured.update(context)
        return "dashboard rendered"

    monkeypatch.setattr(dashboardroute, "Report", FakeReport)
    monkeypatch.setattr(dashboardroute, "render_template", fake_render_template)

    app = Flask(__name__)
    app.config.update(TESTING=True, SECRET_KEY="test")
    from tests.conftest import register_dummy_endpoints

    register_dummy_endpoints(app, skip_names={"dashboard"})
    app.register_blueprint(dashboardroute.dashboardBP)
    client = app.test_client()
    with client.session_transaction() as sess:
        sess["user_id"] = 1

    response = client.get("/dashboard")

    assert response.status_code == 200
    assert response.data == b"dashboard rendered"
    assert captured["template"] == "user/dashboard.html"
    assert captured["summary"] == {
        "total": 4,
        "pending": 1,
        "in_progress": 1,
        "resolved": 2,
    }


def test_my_report_filters_status_type_and_date(monkeypatch):
    from app.routes import my_report_route

    captured = {}

    class FakeReport:
        def get_user_reports(self, user_id):
            return [
                {"id": 1, "status": "pending", "waste_type": "Plastic"},
                {"id": 2, "status": "resolved", "waste_type": "Organic"},
                {"id": 3, "status": "resolved", "waste_type": "Plastic"},
            ]

    def fake_render_template(template, **context):
        captured.update(context)
        return "my reports rendered"

    monkeypatch.setattr(my_report_route, "Report", FakeReport)
    monkeypatch.setattr(my_report_route, "render_template", fake_render_template)

    app = Flask(__name__)
    app.config.update(TESTING=True, SECRET_KEY="test")
    from tests.conftest import register_dummy_endpoints

    register_dummy_endpoints(app, skip_names={"my_report"})
    app.register_blueprint(my_report_route.my_reportBP)
    client = app.test_client()
    with client.session_transaction() as sess:
        sess["user_id"] = 1

    response = client.get("/my_report?status=resolved&waste_type=Plastic&date=oldest")

    assert response.status_code == 200
    assert captured["reports"] == [{"id": 3, "status": "resolved", "waste_type": "Plastic"}]
    assert captured["selected_status"] == "resolved"
    assert captured["selected_type"] == "Plastic"
    assert captured["selected_date"] == "oldest"
