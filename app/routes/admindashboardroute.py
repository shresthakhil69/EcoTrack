from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from app.models.report import Report
from app.models.database import Database

admin_dashboardBP = Blueprint("admin_dashboard", __name__)


def admin_required():
    return 'admin_id' not in session


@admin_dashboardBP.route('/admin/dashboard')
def dashboard():
    if admin_required():
        return redirect(url_for('admin_auth.admin_login'))

    report = Report()
    all_reports = report.find_all(order_by="id DESC")

    db = Database()
    result = db.fetch_one("SELECT COUNT(*) as total FROM users")
    total_users = result['total']
    db.close()

    total = len(all_reports)
    pending = len([r for r in all_reports if r['status'] == 'pending'])
    in_progress = len([r for r in all_reports if r['status'] == 'in_progress'])
    resolved = len([r for r in all_reports if r['status'] == 'resolved'])

    summary = {
        'total_users': total_users,
        'total': total,
        'pending': pending,
        'in_progress': in_progress,
        'resolved': resolved
    }

    return render_template("adminpage/dashboard.html",
                           summary=summary,
                           reports=all_reports)







