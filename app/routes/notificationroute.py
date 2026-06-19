from flask import Blueprint, render_template, request, session, redirect, url_for

notificationBP = Blueprint("notification", __name__)


@notificationBP.route('/notifications')
def notifications():
    return render_template("userpage/notification.html")
 