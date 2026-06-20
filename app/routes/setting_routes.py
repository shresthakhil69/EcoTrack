from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from app.models.user import User
from app.auth import login_required

settingBP = Blueprint("setting", __name__)

@settingBP.route("/setting", methods=['GET', 'POST'])
@login_required
def setting():
    if request.method == 'POST':
        form_type = request.form.get('form_type')
        user_id = session['user_id']
        user = User()

        if form_type == 'profile':
            name = request.form.get('name', '').strip()
            email = request.form.get('email', '').strip()

            if not name or not email:
                flash('Name and email are required.', 'error')
                return redirect(url_for('setting.setting'))

            existing = user.get_by_email(email)
            if existing and existing['id'] != user_id:
                flash('That email is already in use by another account.', 'error')
                return redirect(url_for('setting.setting'))

            user.update_profile(user_id, name, email)

            session['user_name'] = name
            session['user_email'] = email

            flash('Profile updated successfully.', 'success')
            return redirect(url_for('setting.setting'))

        elif form_type == 'password':
            current_password = request.form.get('current_password', '')
            new_password = request.form.get('new_password', '')
            confirm_password = request.form.get('confirm_password', '')

            if not current_password or not new_password or not confirm_password:
                flash('All password fields are required.', 'error')
                return redirect(url_for('setting.setting'))

            if new_password != confirm_password:
                flash('New passwords do not match.', 'error')
                return redirect(url_for('setting.setting'))

            if len(new_password) < 6:
                flash('New password must be at least 6 characters.', 'error')
                return redirect(url_for('setting.setting'))

            user_data = user.get_by_id(user_id)
            if not user.check_password(user_data['password'], current_password):
                flash('Current password is incorrect.', 'error')
                return redirect(url_for('setting.setting'))

            user.update_password(user_id, new_password)
            flash('Password updated successfully.', 'success')

    return render_template("user/setting.html")