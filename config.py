import os

class Config:
    # Bảo vệ form chống CSRF
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'kumiu'

    # Cấu hình kết nối MySQL
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'mysql+pymysql://admin2:admin2@34.124.212.240/calendar_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Cấu hình session timeout (tuỳ chọn)
    PERMANENT_SESSION_LIFETIME = 3600  # 1 giờ

    # Tùy chọn thêm nếu dùng gửi email trong tương lai
    # MAIL_SERVER = 'smtp.gmail.com'
    # MAIL_PORT = 587
    # MAIL_USE_TLS = True
    # MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    # MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')

    # Bật debug cho logger trong SQLAlchemy
    # SQLALCHEMY_ECHO = True
