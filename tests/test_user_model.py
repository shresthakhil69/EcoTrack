from werkzeug.security import check_password_hash

from tests.conftest import FakeDatabase


def test_create_user_hashes_password_and_inserts_user(monkeypatch):
    from app.models import user as user_module

    FakeDatabase.reset()
    monkeypatch.setattr(user_module, "Database", FakeDatabase)

    new_user = user_module.User(
        name="Akhila",
        email="akhila@example.com",
        password="secret123",
        role="user",
    )
    new_user.create_user()

    db = FakeDatabase.instances[0]
    assert len(db.executed) == 1
    query, params = db.executed[0]
    assert "INSERT INTO users" in query
    assert params[0] == "Akhila"
    assert params[1] == "akhila@example.com"
    assert params[2] != "secret123"
    assert check_password_hash(params[2], "secret123")
    assert params[3] == "user"
    assert db.closed is True


def test_get_by_email_returns_matching_user(monkeypatch):
    from app.models import user as user_module

    FakeDatabase.reset()
    FakeDatabase.fetch_one_result = {"id": 1, "email": "student@example.com"}
    monkeypatch.setattr(user_module, "Database", FakeDatabase)

    result = user_module.User().get_by_email("student@example.com")

    db = FakeDatabase.instances[0]
    assert result["id"] == 1
    assert "SELECT * FROM users WHERE email=%s" in db.fetch_one_calls[0][0]
    assert db.fetch_one_calls[0][1] == ("student@example.com",)
    assert db.closed is True


def test_update_profile_executes_expected_update(monkeypatch):
    from app.models import user as user_module

    FakeDatabase.reset()
    monkeypatch.setattr(user_module, "Database", FakeDatabase)

    user_module.User().update_profile(
        user_id=5,
        name="Updated Name",
        email="updated@example.com",
        phone="9800000000",
    )

    query, params = FakeDatabase.instances[0].executed[0]
    assert "UPDATE users SET name=%s, email=%s, phone=%s WHERE id=%s" in query
    assert params == ("Updated Name", "updated@example.com", "9800000000", 5)


def test_update_password_hashes_new_password(monkeypatch):
    from app.models import user as user_module

    FakeDatabase.reset()
    monkeypatch.setattr(user_module, "Database", FakeDatabase)

    user_module.User().update_password(3, "newpass123")

    query, params = FakeDatabase.instances[0].executed[0]
    assert "UPDATE users SET password=%s WHERE id=%s" in query
    assert params[1] == 3
    assert params[0] != "newpass123"
    assert check_password_hash(params[0], "newpass123")
