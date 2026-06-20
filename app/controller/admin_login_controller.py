from flask import request, session, redirect, url_for, flash
from app.models.user import User


def admin_login_data():
    email = request.form.get('email', '').strip()
    password = request.form.get('password', '')

    if not email or not password:
        flash('Email and password are required.', 'error')
        return redirect(url_for('admin_auth.admin_login'))

    user = User()
    user_data = user.get_by_email(email)

    if not user_data:
        flash('No admin account found with that email.', 'error')
        return redirect(url_for('admin_auth.admin_login'))

    if user_data['role'] != 'admin':
        flash('Access denied. Not an admin account.', 'error')
        return redirect(url_for('admin_auth.admin_login'))

    if not user.check_password(user_data['password'], password):
        flash('Incorrect password.', 'error')
        return redirect(url_for('admin_auth.admin_login'))

    # Set admin session
    session['admin_id'] = user_data['id']
    session['admin_name'] = user_data['name']
    session['admin_email'] = user_data['email']

    return redirect(url_for('admin_dashboard.dashboard'))
