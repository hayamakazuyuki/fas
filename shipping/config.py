import os

class BaseConfig(object):
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'secret'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://user:password@mysql/fas?charset=utf8'

    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    
    MAIL_DEFAULT_SENDER = 'noreply@mg.furoshiki.in'
    MAIL_PORT = 587
    MAIL_USE_TLS = True

class ProductionConfig(BaseConfig):
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')

class TestingConfig(BaseConfig):
    TESTING = True
    
class DevelopmentConfig(BaseConfig):
    DEBUG = True
    