from flask import Blueprint, render_template, request, session,redirect,url_for,flash
from app.auth import admin_required

admin_dashboardBP = Blueprint("admin_dashboard", __name__)

@admin_dashboardBP.route('/admin/dashboard')
@admin_required
def dashboard():
    return render_template('admin/dashboard.html')