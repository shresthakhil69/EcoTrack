from flask import Blueprint, render_template, request, session, redirect, url_for

auth_admin = Blueprint("admin_auth", __name__)


@auth_admin.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if 'admin_id' in session:
        return redirect(url_for('admin_dashboard.dashboard'))

    if request.method == 'POST':
        from app.controller.admin_login_controller import admin_login_data
        return admin_login_data()

    return render_template("auth_admin/admin_login.html")


@auth_admin.route('/admin_logout')
def admin_logout():
    session.pop('admin_id', None)
    session.pop('admin_name', None)
    session.pop('admin_email', None)
    return redirect(url_for('home.home'))
