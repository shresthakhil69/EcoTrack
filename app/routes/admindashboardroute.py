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


@admin_dashboardBP.route('/admin/update_status', methods=['POST'])
def update_status():
    if admin_required():
        return redirect(url_for('admin_auth.admin_login'))

    report_id = request.form.get('report_id')
    new_status = request.form.get('status')

    allowed = ['pending', 'in_progress', 'resolved']
    if new_status not in allowed:
        flash('Invalid status.', 'error')
        return redirect(url_for('admin_dashboard.dashboard'))

    # Get report to find the user_id before updating
    report = Report()
    existing = report.find_by_id(report_id)

    if existing:
        report.update_status(report_id, new_status)

        # Trigger notification to the report owner
        from app.controller.notification_controller import create_notification
        create_notification(existing['user_id'], report_id, new_status)

        flash(f'Report #{report_id} status updated to {new_status}.', 'success')
    else:
        flash('Report not found.', 'error')

    return redirect(url_for('admin_dashboard.dashboard'))


@admin_dashboardBP.route('/admin/delete_report', methods=['POST'])
def delete_report():
    if admin_required():
        return redirect(url_for('admin_auth.admin_login'))

    report_id = request.form.get('report_id')
    report = Report()
    report.delete_by_id(report_id)

    flash(f'Report #{report_id} deleted.', 'success')
    return redirect(url_for('admin_dashboard.dashboard'))


@admin_dashboardBP.route('/admin/users')
def users():
    if admin_required():
        return redirect(url_for('admin_auth.admin_login'))

    db = Database()
    all_users = db.fetch_all(
        "SELECT id, name, email, role, reported_on   FROM users ORDER BY reported_on   DESC"
    )
    db.close()

    return render_template("adminpage/users.html", users=all_users)


@admin_dashboardBP.route('/admin/delete_user', methods=['POST'])
def delete_user():
    if admin_required():
        return redirect(url_for('admin_auth.admin_login'))

    user_id = request.form.get('user_id')

    # Don't allow deleting your own admin account
    if int(user_id) == session['admin_id']:
        flash('You cannot delete your own admin account.', 'error')
        return redirect(url_for('admin_dashboard.users'))

    # Delete notifications first
    db = Database()
    db.execute("DELETE FROM notifications WHERE user_id=%s", (user_id,))
    db.close()

    # Delete reports (notifications inside already handled by override)
    report = Report()
    user_reports = report.get_user_reports(user_id)
    for r in user_reports:
        report.delete_by_id(r['id'])

    # Delete user
    db = Database()
    db.execute("DELETE FROM users WHERE id=%s", (user_id,))
    db.close()

    flash('User deleted successfully.', 'success')
    return redirect(url_for('admin_dashboard.users'))


@admin_dashboardBP.route('/admin/warn_user', methods=['POST'])
def warn_user():
    if admin_required():
        return redirect(url_for('admin_auth.admin_login'))

    report_id = request.form.get('report_id')
    warning_message = request.form.get('warning_message', '').strip()

    if not warning_message:
        flash('Warning message cannot be empty.', 'error')
        return redirect(url_for('admin_dashboard.dashboard'))

    report = Report()
    existing = report.find_by_id(report_id)

    if existing:
        from app.controller.notification_controller import create_warning
        create_warning(existing['user_id'], report_id, warning_message)
        flash(f'Warning sent to user for report #{report_id}.', 'success')
    else:
        flash('Report not found.', 'error')

    return redirect(url_for('admin_dashboard.dashboard'))


@admin_dashboardBP.route('/admin/feedback')
def feedback():
    if admin_required():
        return redirect(url_for('admin_auth.admin_login'))

    from app.models.feedback import Feedback
    feedback_model = Feedback()
    all_feedback = feedback_model.get_all_feedback()

    return render_template("adminpage/feedback.html", feedback_list=all_feedback)


@admin_dashboardBP.route('/admin/feedback/update_status', methods=['POST'])
def update_feedback_status():
    if admin_required():
        return redirect(url_for('admin_auth.admin_login'))

    feedback_id = request.form.get('feedback_id')
    new_status = request.form.get('status')

    allowed = ['new', 'reviewed', 'resolved']
    if new_status not in allowed:
        flash('Invalid status.', 'error')
        return redirect(url_for('admin_dashboard.feedback'))

    from app.models.feedback import Feedback
    feedback_model = Feedback()
    feedback_model.update_status(feedback_id, new_status)

    flash('Feedback status updated.', 'success')
    return redirect(url_for('admin_dashboard.feedback'))