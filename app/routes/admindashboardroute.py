from flask import Blueprint, render_template

admin_dashboardBP = Blueprint("admin_dashboard", __name__)

@admin_dashboardBP.route('/admin/dashboard')
def dashboard():
    
        return render_template('admin_auth.admin_login')