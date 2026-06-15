from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from app.models.user import User

settingBP = Blueprint("setting", __name__)
@settingBP.route("/setting", methods=['GET', 'POST'])

def setting():
    if 'user_id' not in session:
        return redirect(url_for('user_auth.login'))

    if request.method == 'POST':
        form_type = request.form.get('form_type')
        user_id = session['user_id']
        user = User()

        # ── Profile Update ──────────────────────────
        if form_type == 'profile':
            name = request.form.get('name', '').strip()
            email = request.form.get('email', '').strip()

            if not name or not email:
                flash('Name and email are required.', 'error')
                return redirect(url_for('setting.setting'))

            # Check email not taken by another user
            existing = user.get_by_email(email)
            if existing and existing['id'] != user_id:
                flash('That email is already in use by another account.', 'error')
                return redirect(url_for('setting.setting'))

            user.update_profile(user_id, name, email)

            # Update session so navbar shows new name immediately
            session['user_name'] = name
            session['user_email'] = email

            flash('Profile updated successfully.', 'success')