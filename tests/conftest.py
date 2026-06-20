"""Shared pytest fixtures for the EcoTrack Flask project.

These tests are designed for the existing EcoTrack codebase without requiring
an active MySQL database. Database calls are replaced with small fake classes
inside each test file using pytest's monkeypatch fixture.
"""

import sys
from pathlib import Path

import pytest
from flask import Blueprint, Flask


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


@pytest.fixture
def app():
    """Create a lightweight Flask app for route/controller unit tests."""
    flask_app = Flask(
        __name__,
        template_folder=str(PROJECT_ROOT / "app" / "templates"),
        static_folder=str(PROJECT_ROOT / "app" / "static"),
    )
    flask_app.config.update(TESTING=True, SECRET_KEY="test-secret-key")
    register_dummy_endpoints(flask_app)
    return flask_app


@pytest.fixture
def client(app):
    return app.test_client()


def register_dummy_endpoints(flask_app, skip_names=None):
    """Register endpoint names used by redirect(url_for(...)) in EcoTrack.

    Use skip_names when a test registers the real blueprint with the same name.
    Example: register_dummy_endpoints(app, skip_names={"dashboard"})
    """
    skip_names = set(skip_names or [])

    blueprints = []

    if "user_auth" not in skip_names:
        user_auth = Blueprint("user_auth", __name__)

        @user_auth.route("/login")
        def login():
            return "login page"

        @user_auth.route("/register")
        def register():
            return "register page"

        @user_auth.route("/logout")
        def logout():
            return "logout page"

        blueprints.append(user_auth)

    if "dashboard" not in skip_names:
        dashboard_bp = Blueprint("dashboard", __name__)

        @dashboard_bp.route("/dashboard")
        def dashboard():
            return "dashboard page"

        blueprints.append(dashboard_bp)

    if "home" not in skip_names:
        home_bp = Blueprint("home", __name__)

        @home_bp.route("/")
        def home():
            return "home page"

        blueprints.append(home_bp)

    if "admin_auth" not in skip_names:
        admin_auth = Blueprint("admin_auth", __name__)

        @admin_auth.route("/admin_login")
        def admin_login():
            return "admin login page"

        blueprints.append(admin_auth)

    if "admin_dashboard" not in skip_names:
        admin_dashboard_bp = Blueprint("admin_dashboard", __name__)

        @admin_dashboard_bp.route("/admin/dashboard")
        def dashboard():
            return "admin dashboard page"

        @admin_dashboard_bp.route("/admin/users")
        def users():
            return "admin users page"

        @admin_dashboard_bp.route("/admin/feedback")
        def feedback():
            return "admin feedback page"

        blueprints.append(admin_dashboard_bp)

    if "report_success" not in skip_names:
        report_success_bp = Blueprint("report_success", __name__)

        @report_success_bp.route("/report_success")
        def report_success():
            return "report success page"

        blueprints.append(report_success_bp)

    if "my_report" not in skip_names:
        my_report_bp = Blueprint("my_report", __name__)

        @my_report_bp.route("/my_report")
        def my_report():
            return "my report page"

        blueprints.append(my_report_bp)

    if "setting" not in skip_names:
        setting_bp = Blueprint("setting", __name__)

        @setting_bp.route("/setting")
        def setting():
            return "setting page"

        blueprints.append(setting_bp)

    if "help_support" not in skip_names:
        help_support_bp = Blueprint("help_support", __name__)

        @help_support_bp.route("/help_support")
        def help_support():
            return "help support page"

        blueprints.append(help_support_bp)

    for bp in blueprints:
        flask_app.register_blueprint(bp)


class FakeDatabase:
    """Tiny fake database used by model tests."""

    instances = []
    fetch_one_result = None
    fetch_all_result = []

    def __init__(self):
        self.executed = []
        self.fetch_one_calls = []
        self.fetch_all_calls = []
        self.closed = False
        FakeDatabase.instances.append(self)

    @classmethod
    def reset(cls):
        cls.instances = []
        cls.fetch_one_result = None
        cls.fetch_all_result = []

    def execute(self, query, params=None):
        self.executed.append((" ".join(query.split()), params))

    def fetch_one(self, query, params=None):
        self.fetch_one_calls.append((" ".join(query.split()), params))
        return FakeDatabase.fetch_one_result

    def fetch_all(self, query, params=None):
        self.fetch_all_calls.append((" ".join(query.split()), params))
        return FakeDatabase.fetch_all_result

    def close(self):
        self.closed = True
