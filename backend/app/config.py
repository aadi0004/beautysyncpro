import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Database configuration
    DB_HOST = os.getenv('DB_HOST', 'db')
    DB_USER = os.getenv('DB_USER', 'root')
    DB_PASSWORD = os.getenv('DB_PASSWORD', 'password')  # Should match docker-compose.yml
    DB_NAME = os.getenv('DB_NAME', 'beautysyncpro')
    SQLALCHEMY_DATABASE_URI = (
        f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:3306/{DB_NAME}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Flask environment
    FLASK_ENV = os.getenv('FLASK_ENV', 'production')

    # Secret key for security
    SECRET_KEY = os.getenv('SECRET_KEY', os.urandom(24).hex())  # Generate a random key if not set

    # Email configuration
    MAIL_SERVER = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.getenv('MAIL_PORT', 587))
    MAIL_USE_TLS = os.getenv('MAIL_USE_TLS', 'True').lower() == 'true'  # Simplified logic
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')

    # Validation for critical settings
    def __init__(self):
        if not self.SECRET_KEY:
            raise ValueError("SECRET_KEY must be set in the environment for security.")
        if self.FLASK_ENV == 'production' and (not self.MAIL_USERNAME or not self.MAIL_PASSWORD):
            raise ValueError("MAIL_USERNAME and MAIL_PASSWORD must be set in production for email functionality.")