from flask import request, session, redirect, url_for, flash
from app.model.user import User


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

    