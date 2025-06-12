import threading
import time
from datetime import datetime, timedelta
from models import db, Event, User
from email_service import send_reminder_email


def check_and_send_reminders(app):

    with app.app_context():
        try:
            now = datetime.now()

            # Tìm các sự kiện cần nhắc nhở
            events_to_remind = Event.query.join(User).filter(
                Event.start > now,
                Event.start <= now + timedelta(minutes=60),  # Kiểm tra trong 60 phút tới
                Event.reminder_sent == False  # Chưa gửi nhắc nhở
            ).all()

            for event in events_to_remind:
                # Tính thời gian còn lại đến sự kiện
                time_until_event = (event.start - now).total_seconds() / 60  # phút

                # Nếu đến thời gian nhắc nhở
                if time_until_event <= event.reminder_minutes_before:
                    user = User.query.get(event.user_id)
                    if user and user.email:
                        success = send_reminder_email(user.email, event)
                        if success:
                            # Đánh dấu đã gửi nhắc nhở
                            event.reminder_sent = True
                            db.session.commit()
                            print(f"Reminder sent for event: {event.title}")

        except Exception as e:
            print(f"Error in reminder scheduler: {e}")


def start_reminder_scheduler(app):

    def run_scheduler():
        while True:
            check_and_send_reminders(app)
            time.sleep(300)  # Kiểm tra mỗi 5 phút

    thread = threading.Thread(target=run_scheduler)
    thread.daemon = True
    thread.start()
    print("Reminder scheduler started!")