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

    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'caoducthanh18@gmail.com'  # Thay bằng email của bạn
    MAIL_PASSWORD = 'your_app_password'     # App Password, KHÔNG phải mật khẩu thường
    MAIL_DEFAULT_SENDER = 'caoducthanh18@gmail.com'



