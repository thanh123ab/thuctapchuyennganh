import os
class Config:

    SECRET_KEY = os.environ.get('SECRET_KEY') or 'kumiu'


    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'mysql+pymysql://admin2:admin2@34.124.212.240/calendar_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


    PERMANENT_SESSION_LIFETIME = 3600  # 1 giờ

    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'caoducthanh18@gmail.com'
    MAIL_PASSWORD = 'dfhq wmzd tfou xwwn'
    MAIL_DEFAULT_SENDER = 'caoducthanh18@gmail.com'