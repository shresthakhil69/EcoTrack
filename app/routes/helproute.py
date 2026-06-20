from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from app.models.feedback import Feedback
from app.auth import login_required

helpBP = Blueprint("help_support", __name__)


@helpBP.route('/help_support', methods=['GET', 'POST'])
@login_required
def help_support():
    user_id = session['user_id']

    if request.method == 'POST':
        subject = request.form.get('subject', '').strip()
        message = request.form.get('message', '').strip()

        if not subject or not message:
            flash('Subject and message are required.', 'error')
            return redirect(url_for('help_support.help_support'))

        feedback = Feedback(
            user_id=user_id,
            subject=subject,
            message=message
        )
        feedback.save()

        flash('Your feedback has been sent to the admin. Thank you!', 'success')
        return redirect(url_for('help_support.help_support'))

    feedback = Feedback()
    my_feedback = feedback.get_user_feedback(user_id)

    return render_template("user/help_support.html", my_feedback=my_feedback)