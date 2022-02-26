from dotenv import load_dotenv
import os

load_dotenv()


class MailConfig():
    # Flask-Mail SMTP server settings
    MAIL_SERVER = '127.0.0.1'
    MAIL_PORT = 1025
    MAIL_USE_SSL = False
    MAIL_USE_TLS = False
    MAIL_USERNAME = 'email@example.com'     
    MAIL_PASSWORD = 'password'
    MAIL_DEFAULT_SENDER = '"MyApp" <noreply@example.com>'

    # Flask-User settings
    USER_APP_NAME = "Flask-User Basic App"      # Shown in and email templates and page footers
    USER_ENABLE_EMAIL = True        # Enable email aution
    USER_ENABLE_USERNAME = False    # Disable username authentication
    USER_EMAIL_SENDER_NAME = USER_APP_NAME
    USER_EMAIL_SENDER_EMAIL = "noreply@example.com"
    USER_ENABLE_USERNAME =False

class ConfigDebug(MailConfig):
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI_AZURE')
    SECRET_KEY = os.getenv('SECRET_KEY')

    DEBUG=True
    TESTING=False
    

class ConfigTest(MailConfig):
    SERVER_NAME = "BankApp.com"
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI_LOCAL')
    WTF_CSRF_ENABLED = False
    WTF_CSRF_METHODS = []  # This is the magic
    TESTING = True
