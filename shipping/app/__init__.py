from flask import Flask

from .extentions import db, mail
from .views import shipping


def create_app():
    app = Flask(__name__)

    if app.config['ENV'] == 'production':
        app.config.from_object('config.ProductionConfig')
    
    elif app.config['ENV'] == 'testing':
        app.config.from_object('config.TestingConfig')

    else:
        app.config.from_object('config.DevelopmentConfig')


    db.init_app(app)
    mail.init_app(app)

    app.register_blueprint(shipping)

    return app
