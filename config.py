import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-here'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///./test.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True
    UPLOAD_FOLDER = '/path/to/uploads'
    MAIL_SERVER = 'smtp.example.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    SESSION_TYPE = 'filesystem'
    PERMANENT_SESSION_LIFETIME = 3600
