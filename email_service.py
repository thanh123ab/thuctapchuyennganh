
from flask_mail import Mail, Message
from flask import current_app

mail = Mail()


def send_email(to, subject, template):

    try:
        msg = Message(
            subject=subject,
            recipients=[to],
            html=template,
            sender=current_app.config['MAIL_DEFAULT_SENDER']
        )
        mail.send(msg)
        print(f"Email sent successfully to {to}")
        return True
    except Exception as e:
        print(f"Failed to send email: {e}")
        return False


def send_reminder_email(user_email, event):

    subject = f" Nhắc nhở: {event.title}"


    html_template = f"""
    <html>
    <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
        <div style="background-color: #f8f9fa; padding: 20px; border-radius: 10px;">
            <h2 style="color: #007bff; margin-bottom: 20px;"> Nhắc nhở sự kiện</h2>

            <div style="background-color: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                <h3 style="color: #333; margin-top: 0;">{event.title}</h3>

                <p><strong> Mô tả:</strong> {event.description or 'Không có mô tả'}</p>

                <p><strong>Thời gian bắt đầu:</strong> {event.start.strftime('%d/%m/%Y lúc %H:%M')}</p>

                {f'<p><strong> Thời gian kết thúc:</strong> {event.end.strftime("%d/%m/%Y lúc %H:%M")}</p>' if event.end else ''}

                <div style="margin-top: 20px; padding: 15px; background-color: #e3f2fd; border-radius: 5px;">
                    <p style="margin: 0; color: #1976d2;">
                         Sự kiện sẽ diễn ra trong <strong>{event.reminder_minutes_before} phút</strong> nữa!
                    </p>
                </div>
            </div>

            <p style="text-align: center; margin-top: 20px; color: #666; font-size: 14px;">
                Email này được gửi từ hệ thống quản lý lịch của bạn
            </p>
        </div>
    </body>
    </html>
    """

    return send_email(user_email, subject, html_template)