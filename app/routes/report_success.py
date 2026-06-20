from flask import Blueprint, render_template
from app.auth import login_required

report_successBP = Blueprint("report_success", __name__)

@report_successBP.route("/report_success")
@login_required
def report_success():
    return render_template("user/report_success.html")