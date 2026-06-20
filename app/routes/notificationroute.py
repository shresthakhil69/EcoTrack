from flask import Blueprint, render_template, session
from app.models.notification import Notification
from app.auth import login_required

notificationBP = Blueprint("notification", __name__)

@notificationBP.route('/notifications')
@login_required
def notifications():
    notif = Notification()
    user_notifications = notif.get_user_notifications(session['user_id'])

    for n in user_notifications:
        if not n['is_read']:
            notif.mark_as_read(n['id'])

    return render_template("user/notification.html", notifications=user_notifications)