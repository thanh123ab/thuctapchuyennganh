import os

class Config:
    SECRET_KEY = 'kumiu'  # để bảo vệ form CSRF
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://admin:admin@34.124.212.240/calendar_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
