from tests.conftest import FakeDatabase


def test_report_save_inserts_report(monkeypatch):
    from app.models import report as report_module

    FakeDatabase.reset()
    monkeypatch.setattr(report_module, "Database", FakeDatabase)

    report = report_module.Report(
        user_id=2,
        waste_type="Plastic",
        description="Plastic waste near park",
        location="Kathmandu",
        image_path="plastic.jpg",
    )
    report.save()

    query, params = FakeDatabase.instances[0].executed[0]
    assert "INSERT INTO reports" in query
    assert params == (2, "Plastic", "Plastic waste near park", "Kathmandu", "plastic.jpg", "pending")


def test_get_user_reports_fetches_reports_for_user(monkeypatch):
    from app.models import report as report_module

    FakeDatabase.reset()
    FakeDatabase.fetch_all_result = [{"id": 10, "user_id": 2, "status": "pending"}]
    monkeypatch.setattr(report_module, "Database", FakeDatabase)

    reports = report_module.Report().get_user_reports(2)

    assert reports == [{"id": 10, "user_id": 2, "status": "pending"}]
    query, params = FakeDatabase.instances[0].fetch_all_calls[0]
    assert "FROM reports WHERE user_id=%s" in query
    assert params == (2,)


def test_search_user_reports_uses_like_for_type_location_and_description(monkeypatch):
    from app.models import report as report_module

    FakeDatabase.reset()
    monkeypatch.setattr(report_module, "Database", FakeDatabase)

    report_module.Report().search_user_reports(9, "glass")

    query, params = FakeDatabase.instances[0].fetch_all_calls[0]
    assert "waste_type LIKE %s" in query
    assert "location LIKE %s" in query
    assert "description LIKE %s" in query
    assert params == (9, "%glass%", "%glass%", "%glass%")


def test_update_status_executes_status_update(monkeypatch):
    from app.models import report as report_module

    FakeDatabase.reset()
    monkeypatch.setattr(report_module, "Database", FakeDatabase)

    report_module.Report().update_status(4, "resolved")

    query, params = FakeDatabase.instances[0].executed[0]
    assert "UPDATE reports SET status=%s WHERE id=%s" in query
    assert params == ("resolved", 4)


def test_delete_report_removes_notifications_before_report(monkeypatch):
    from app.models import report as report_module

    FakeDatabase.reset()
    monkeypatch.setattr(report_module, "Database", FakeDatabase)

    report_module.Report().delete_by_id(12)

    executed = FakeDatabase.instances[0].executed
    assert "DELETE FROM notifications WHERE report_id=%s" in executed[0][0]
    assert executed[0][1] == (12,)
    assert "DELETE FROM reports WHERE id=%s" in executed[1][0]
    assert executed[1][1] == (12,)


def test_update_report_without_image_keeps_existing_image(monkeypatch):
    from app.models import report as report_module

    FakeDatabase.reset()
    monkeypatch.setattr(report_module, "Database", FakeDatabase)

    report_module.Report().update_report(
        report_id=7,
        location="Lalitpur",
        waste_type="Organic",
        description="Food waste",
        image_file=None,
    )

    query, params = FakeDatabase.instances[0].executed[0]
    assert "image_path" not in query
    assert params == ("Lalitpur", "Organic", "Food waste", 7)
