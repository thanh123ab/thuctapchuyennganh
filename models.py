from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    name = db.Column(db.String(100))
    password = db.Column(db.String(200), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    email_notifications = db.Column(db.Boolean, default=True, nullable=False)  # Có muốn nhận email không
    events = db.relationship('Event', backref='user', lazy=True)
    logs = db.relationship('Log', backref='user', lazy=True)


class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    start = db.Column(db.DateTime, nullable=False)
    end = db.Column(db.DateTime, nullable=False)
    reminder_minutes_before = db.Column(db.Integer, default=15)  # Thay đổi default từ 0 thành 15
    repeat_type = db.Column(db.String(20), default='none')
    reminder_sent = db.Column(db.Boolean, default=False, nullable=False)


    reminder_sent_at = db.Column(db.DateTime, nullable=True)  # Lưu thời gian đã gửi email

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


    def reset_reminder(self):

        self.reminder_sent = False
        self.reminder_sent_at = None


class Log(db.Model):
    __tablename__ = 'logs'
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user_name = db.Column(db.String(100))
    action = db.Column(db.String(100))
    details = db.Column(db.Text)


# T
class EmailLog(db.Model):
    __tablename__ = 'email_logs'
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)
    email_type = db.Column(db.String(50), default='reminder')  # reminder, notification, etc.
    email_address = db.Column(db.String(150), nullable=False)
    subject = db.Column(db.String(200))
    status = db.Column(db.String(20), default='sent')  # sent, failed
    error_message = db.Column(db.Text, nullable=True)

    # Relationships
    user = db.relationship('User', backref='email_logs')
    event = db.relationship('Event', backref='email_logs')