from flask import Blueprint, render_template, session, redirect, url_for
from app.models.database import Database

dashboardBP = Blueprint("dashboard", __name__)

@dashboardBP.route("/dashboard")
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('user_auth.login'))

    user_id = session['user_id']
    
    db = Database()
    user_reports = db.fetch_all("SELECT * FROM reports WHERE user_id = %s", (user_id,))
    db.close()

    total = len(user_reports)
    pending = len([r for r in user_reports if r['status'] == 'pending'])
    in_progress = len([r for r in user_reports if r['status'] == 'in_progress'])
    resolved = len([r for r in user_reports if r['status'] == 'resolved'])

    summary = {
        'total': total,
        'pending': pending,
        'in_progress': in_progress,
        'resolved': resolved
    }

    recent_reports = user_reports[:5]

    return render_template("user/dashboard.html",
                           summary=summary,
                           recent_reports=recent_reports)