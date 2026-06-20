from flask import Blueprint, render_template, request, session, redirect, url_for
from app.models.notification import Notification

notificationBP = Blueprint("notification", __name__)


@notificationBP.route('/notifications')
def notifications():
    if 'user_id' not in session:
        return redirect(url_for('user_auth.login'))

    notif = Notification()
    user_notifications = notif.get_user_notifications(session['user_id'])

    # Mark all as read
    for n in user_notifications:
        if not n['is_read']:
            notif.mark_as_read(n['id'])

    return render_template("user/notification.html", notifications=user_notifications)
