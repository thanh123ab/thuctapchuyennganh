from flask_mail import Mail, Message
from flask import current_app

mail = Mail()


def send_reminder_email(to_email, event):
    subject = f"Nhắc nhở: {event.title}"
    body = f"Sự kiện: {event.title}\nThời gian bắt đầu: {event.start.strftime('%H:%M %d/%m/%Y')}"

    try:
        msg = Message(
            subject=subject,
            recipients=[to_email],
            body=body,  # không cần html nếu muốn gửi đơn giản
            sender=current_app.config['MAIL_DEFAULT_SENDER']
        )
        mail.send(msg)
        print(f"Sent reminder email to {to_email}")
        return True
    except Exception as e:
        print(f"Failed to send email to {to_email}: {str(e)}")
        return False
