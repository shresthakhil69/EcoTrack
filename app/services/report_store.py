import json
import os
from datetime import datetime, timezone

from flask import current_app


VALID_STATUSES = {"pending", "in_progress", "resolved"}
STATUS_LABELS = {
    "pending": "Pending",
    "in_progress": "In Progress",
    "resolved": "Resolved",
}


def _reports_data_path():
    data_dir = os.path.join(current_app.root_path, "data")
    os.makedirs(data_dir, exist_ok=True)
    return os.path.join(data_dir, "reports.json")


def normalize_status(status):
    value = str(status or "pending").strip().lower()
    value = value.replace(" ", "_").replace("-", "_")
    return value if value in VALID_STATUSES else "pending"


def status_label(status):
    return STATUS_LABELS.get(normalize_status(status), "Pending")


def _normalize_report(report, index):
    normalized = dict(report)

    try:
        normalized["id"] = int(normalized.get("id") or index + 1)
    except (TypeError, ValueError):
        normalized["id"] = index + 1

    normalized["status"] = normalize_status(normalized.get("status"))
    normalized["status_label"] = status_label(normalized["status"])
    normalized["status_class"] = normalized["status"]
    normalized.setdefault("user_id", None)
    normalized.setdefault("location", "")
    normalized.setdefault("waste_type", "")
    normalized.setdefault("description", "")
    normalized.setdefault("image", None)
    normalized.setdefault("reported_on", "")
    return normalized


def load_reports():
    path = _reports_data_path()
    try:
        with open(path, "r", encoding="utf-8") as file:
            reports = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

    if not isinstance(reports, list):
        return []

    return [
        _normalize_report(report, index)
        for index, report in enumerate(reports)
        if isinstance(report, dict)
    ]


def save_reports(reports):
    normalized = [
        _normalize_report(report, index)
        for index, report in enumerate(reports)
        if isinstance(report, dict)
    ]

    with open(_reports_data_path(), "w", encoding="utf-8") as file:
        json.dump(normalized, file, ensure_ascii=False, indent=2)

    return normalized


def next_report_id(reports):
    ids = []
    for report in reports:
        try:
            ids.append(int(report.get("id")))
        except (TypeError, ValueError):
            continue
    return max(ids, default=0) + 1


def add_report(report):
    reports = load_reports()
    new_report = dict(report)
    new_report["id"] = next_report_id(reports)
    new_report["status"] = normalize_status(new_report.get("status"))
    new_report.setdefault(
        "reported_on",
        datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
    )

    reports.append(new_report)
    return save_reports(reports)[-1]


def find_report(report_id):
    try:
        report_id = int(report_id)
    except (TypeError, ValueError):
        return None

    for report in load_reports():
        if report["id"] == report_id:
            return report
    return None


def update_report_status(report_id, status):
    try:
        report_id = int(report_id)
    except (TypeError, ValueError):
        return False

    reports = load_reports()
    updated = False
    for report in reports:
        if report["id"] == report_id:
            report["status"] = normalize_status(status)
            updated = True
            break

    if updated:
        save_reports(reports)
    return updated


def delete_report(report_id):
    try:
        report_id = int(report_id)
    except (TypeError, ValueError):
        return None

    reports = load_reports()
    remaining = []
    deleted = None
    for report in reports:
        if report["id"] == report_id and deleted is None:
            deleted = report
        else:
            remaining.append(report)

    if deleted is not None:
        save_reports(remaining)

    return deleted


def report_belongs_to_user(report, user_id):
    stored_user_id = report.get("user_id")
    if stored_user_id in (None, ""):
        return True
    return str(stored_user_id) == str(user_id)


def reports_for_user(user_id):
    return [report for report in load_reports() if report_belongs_to_user(report, user_id)]


def delete_reports_for_user(user_id):
    reports = load_reports()
    deleted = [report for report in reports if report_belongs_to_user(report, user_id)]
    remaining = [report for report in reports if not report_belongs_to_user(report, user_id)]
    save_reports(remaining)
    return deleted