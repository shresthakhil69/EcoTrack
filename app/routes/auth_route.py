from flask import Blueprint, render_template, request, session, redirect, url_for

auth_user = Blueprint("user_auth", __name__)


@auth_user.route('/register', methods=['GET', 'POST'])
def register():
    if 'user_id' in session:
        return redirect(url_for('home.home'))

    if request.method == 'POST':
        from app.controller.user_login_controller import register_controller
        return register_controller()

    return render_template("auth_user/register.html")


@auth_user.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        return redirect(url_for('home.home'))

    if request.method == 'POST':
        from app.controller.user_login_controller import login_controller
        return login_controller()

    return render_template("auth_user/login.html")


@auth_user.route('/logout')
def logout():
    from app.controller.user_login_controller import logout_controller
    return logout_controller()
