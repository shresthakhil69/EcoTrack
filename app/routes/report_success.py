from flask import Flask, Blueprint,render_template

report_successBP= Blueprint("report_success", __name__)

@report_successBP.route("/report_success")
def report_success():
    return render_template("user/report_success.html")