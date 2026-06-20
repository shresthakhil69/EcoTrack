from tests.conftest import FakeDatabase


def test_notification_save_inserts_notification(monkeypatch):
    from app.models import notification as notification_module

    FakeDatabase.reset()
    monkeypatch.setattr(notification_module, "Database", FakeDatabase)

    notification_module.Notification(
        user_id=1,
        report_id=5,
        message="Status updated",
        type="status_update",
    ).save()

    query, params = FakeDatabase.instances[0].executed[0]
    assert "INSERT INTO notifications" in query
    assert params == (1, 5, "Status updated", "status_update")


def test_notification_mark_as_read_updates_read_flag(monkeypatch):
    from app.models import notification as notification_module

    FakeDatabase.reset()
    monkeypatch.setattr(notification_module, "Database", FakeDatabase)

    notification_module.Notification().mark_as_read(8)

    query, params = FakeDatabase.instances[0].executed[0]
    assert "UPDATE notifications SET is_read=1 WHERE id=%s" in query
    assert params == (8,)


def test_create_notification_builds_status_message(monkeypatch):
    from app.controller import notification_controller

    saved = {}

    class FakeNotification:
        def __init__(self, user_id=None, report_id=None, message=None, type="status_update"):
            saved["user_id"] = user_id
            saved["report_id"] = report_id
            saved["message"] = message
            saved["type"] = type

        def save(self):
            saved["saved"] = True

    monkeypatch.setattr(notification_controller, "Notification", FakeNotification)

    notification_controller.create_notification(user_id=3, report_id=11, new_status="resolved")

    assert saved["user_id"] == 3
    assert saved["report_id"] == 11
    assert "has been resolved" in saved["message"]
    assert saved["type"] == "status_update"
    assert saved["saved"] is True


def test_create_warning_builds_warning_notification(monkeypatch):
    from app.controller import notification_controller

    saved = {}

    class FakeNotification:
        def __init__(self, user_id=None, report_id=None, message=None, type="status_update"):
            saved.update(user_id=user_id, report_id=report_id, message=message, type=type)

        def save(self):
            saved["saved"] = True

    monkeypatch.setattr(notification_controller, "Notification", FakeNotification)

    notification_controller.create_warning(2, 9, "Please upload a clear photo")

    assert saved["user_id"] == 2
    assert saved["report_id"] == 9
    assert "Warning" in saved["message"]
    assert "Please upload a clear photo" in saved["message"]
    assert saved["type"] == "warning"


def test_feedback_save_and_update_status(monkeypatch):
    from app.models import feedback as feedback_module

    FakeDatabase.reset()
    monkeypatch.setattr(feedback_module, "Database", FakeDatabase)

    feedback_module.Feedback(user_id=1, subject="Help", message="Need support").save()
    save_query, save_params = FakeDatabase.instances[0].executed[0]
    assert "INSERT INTO feedback" in save_query
    assert save_params == (1, "Help", "Need support", "new")

    feedback_module.Feedback().update_status(4, "resolved")
    update_query, update_params = FakeDatabase.instances[1].executed[0]
    assert "UPDATE feedback SET status=%s WHERE id=%s" in update_query
    assert update_params == ("resolved", 4)
