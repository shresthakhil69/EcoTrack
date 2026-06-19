from flask import Blueprint, render_template, request, session

admin_dashboardBP = Blueprint("admin_dashboard", __name__)

def admin_required():
    return 'admin_id' not in session


@admin_dashboardBP.route('/admin/dashboard')
def dashboard():
    
        return render_template('admin_auth.admin_login')