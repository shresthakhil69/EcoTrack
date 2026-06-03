from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.models.database import Database
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()
auth = Blueprint("auth", __name__)

@auth.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]

        hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")

        db = Database()
        cursor = db.get_cursor()
        cursor.execute("INSERT INTO users (name, email, password) V-ALUES (%s, %s, %s)",
                      (name, email, hashed_password))
        db.commit()
        db.close()

        flash("Registration successful! Please login.", "success")
        return redirect(url_for("auth.login"))

    return render_template("auth/register.html")

@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        db = Database()
        cursor = db.get_cursor()
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()
        db.close()

        if user and bcrypt.check_password_hash(user["password"], password):
            session["user_id"] = user["id"]
            session["user_name"] = user["name"]
            session["role"] = user["role"]
            flash("Login successful!", "success")
            return redirect(url_for("home.dashboard"))
        else:
            flash("Wrong email or password!", "danger")

    return render_template("auth/login.html")

@auth.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("auth.login"))


@auth.route('/admin/login')
def admin_login():
      return render_template('admin/login.html')