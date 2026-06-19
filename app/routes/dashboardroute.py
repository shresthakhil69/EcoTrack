from flask import Blueprint, render_template, session, redirect, url_for


dashboardBP = Blueprint("dashboard", __name__)
def dashboard():
             return render_template("userpage/dashboard.html")
