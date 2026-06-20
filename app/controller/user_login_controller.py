from flask import request, session, redirect, url_for, flash
from app.models.user import User


def register_controller():
    name = request.form.get('name', '').strip()
    email = request.form.get('email', '').strip()
    password = request.form.get('password', '')
    confirm_password = request.form.get('confirm_password', '')

    # Basic validation
    if not name or not email or not password:
        flash('All fields are required.', 'error')
        return redirect(url_for('user_auth.register'))

    if password != confirm_password:
        flash('Passwords do not match.', 'error')
        return redirect(url_for('user_auth.register'))

    if len(password) < 6:
        flash('Password must be at least 6 characters.', 'error')
        return redirect(url_for('user_auth.register'))

    user = User()

    # Check if email already exists
    existing = user.get_by_email(email)
    if existing:
        flash('An account with this email already exists.', 'error')
        return redirect(url_for('user_auth.register'))

    # Create the user
    new_user = User(name=name, email=email, password=password, role='user')
    new_user.create_user()

    flash('Account created successfully! Please log in.', 'success')
    return redirect(url_for('user_auth.login'))


def login_controller():
    email = request.form.get('email', '').strip()
    password = request.form.get('password', '')

    if not email or not password:
        flash('Email and password are required.', 'error')
        return redirect(url_for('user_auth.login'))

    user = User()
    user_data = user.get_by_email(email)

    if not user_data:
        flash('No account found with that email.', 'error')
        return redirect(url_for('user_auth.login'))

    if not user.check_password(user_data['password'], password):
        flash('Incorrect password. Please try again.', 'error')
        return redirect(url_for('user_auth.login'))

    # Set session
    session['user_id'] = user_data['id']
    session['user_name'] = user_data['name']
    session['user_email'] = user_data['email']
    session['user_role'] = user_data['role']

    return redirect(url_for('dashboard.dashboard'))


def logout_controller():
    session.clear()
    flash('You have been logged out.', 'success')
    return redirect(url_for('home.home'))
