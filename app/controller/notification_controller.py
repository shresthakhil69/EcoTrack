from app.models.notification import Notification


def create_notification(user_id, report_id, new_status):
    """Called whenever admin updates a report status."""

    status_messages = {
        'pending': 'Your report #{} has been received and is pending review.',
        'in_progress': 'Your report #{} is now being reviewed and is in progress.',
        'resolved': 'Your report #{} has been resolved. Thank you for reporting!'
    }

    message = status_messages.get(new_status, 'Your report #{} has been updated.').format(report_id)

    notification = Notification(
        user_id=user_id,
        report_id=report_id,
        message=message
    )
    notification.save()
    
def create_warning(user_id, report_id, warning_message):
    """Called when admin warns a user about an inappropriate report."""

    full_message = f"⚠ Warning regarding your report #{report_id}: {warning_message}"

    notification = Notification(
        user_id=user_id,
        report_id=report_id,
        message=full_message,
        type='warning'
    )
    notification.save()