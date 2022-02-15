import os

class BaseConfig(object):
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'secret'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://user:password@mysql/fas?charset=utf8'

    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER')
    MAIL_PORT = os.environ.get('MAIL_PORT')
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS')

    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')

class ProductionConfig(BaseConfig):
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')

class TestingConfig(BaseConfig):
    TESTING = True
    
class DevelopmentConfig(BaseConfig):
    DEBUG = True
    