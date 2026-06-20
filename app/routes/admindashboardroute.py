from flask import Blueprint, render_template, request, session,redirect,url_for,flash

admin_dashboardBP = Blueprint("admin_dashboard", __name__)

def admin_required():
    return 'admin_id' not in session


@admin_dashboardBP.route('/admin/dashboard')
def dashboard():
    if admin_required():
        return redirect(url_for('admin_auth.admin_login'))