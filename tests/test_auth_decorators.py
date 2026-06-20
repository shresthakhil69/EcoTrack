from flask import Blueprint


def test_login_required_redirects_when_user_not_logged_in(app):
    from app.auth import login_required

    protected_bp = Blueprint("protected_user", __name__)

    @protected_bp.route("/protected-user")
    @login_required
    def protected_user():
        return "allowed"

    app.register_blueprint(protected_bp)
    client = app.test_client()

    response = client.get("/protected-user")

    assert response.status_code == 302
    assert "/login" in response.headers["Location"]


def test_login_required_allows_logged_in_user(app):
    from app.auth import login_required

    protected_bp = Blueprint("protected_user_ok", __name__)

    @protected_bp.route("/protected-user-ok")
    @login_required
    def protected_user_ok():
        return "allowed"

    app.register_blueprint(protected_bp)
    client = app.test_client()
    with client.session_transaction() as sess:
        sess["user_id"] = 1

    response = client.get("/protected-user-ok")

    assert response.status_code == 200
    assert response.data == b"allowed"


def test_admin_required_redirects_when_admin_not_logged_in(app):
    from app.auth import admin_required

    protected_bp = Blueprint("protected_admin", __name__)

    @protected_bp.route("/protected-admin")
    @admin_required
    def protected_admin():
        return "admin allowed"

    app.register_blueprint(protected_bp)
    client = app.test_client()

    response = client.get("/protected-admin")

    assert response.status_code == 302
    assert "/admin_login" in response.headers["Location"]


def test_admin_required_allows_logged_in_admin(app):
    from app.auth import admin_required

    protected_bp = Blueprint("protected_admin_ok", __name__)

    @protected_bp.route("/protected-admin-ok")
    @admin_required
    def protected_admin_ok():
        return "admin allowed"

    app.register_blueprint(protected_bp)
    client = app.test_client()
    with client.session_transaction() as sess:
        sess["admin_id"] = 1

    response = client.get("/protected-admin-ok")

    assert response.status_code == 200
    assert response.data == b"admin allowed"
