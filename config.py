import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-here'  # Change in production
    SQLALCHEMY_DATABASE_URI = 'sqlite:///healthconnect.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False