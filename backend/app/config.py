import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    DB_HOST = os.getenv('DB_HOST', 'db')
    SQLALCHEMY_DATABASE_URI = f"mysql+mysqlconnector://root:aditya230f@{DB_HOST}:3306/beautysyncpro"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    FLASK_ENV = os.getenv('FLASK_ENV', 'production')

    SECRET_KEY = os.getenv('SECRET_KEY', 'default-secret-key')
    # SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    # SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.getenv('MAIL_PORT', 587))
    MAIL_USE_TLS = os.getenv('MAIL_USE_TLS', 'True') == 'True'
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')