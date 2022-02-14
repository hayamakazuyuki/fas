from flask import Flask

from .extentions import db, mail, login_manager
from .views import shipping
from .user.views import user


def create_app():
    app = Flask(__name__)

    if app.config['ENV'] == 'production':
        app.config.from_object('config.ProductionConfig')
    
    elif app.config['ENV'] == 'testing':
        app.config.from_object('config.TestingConfig')

    else:
        app.config.from_object('config.DevelopmentConfig')


    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    login_manager.login_view = 'user.login'
    login_manager.login_message = False

    app.register_blueprint(shipping)
    app.register_blueprint(user)

    return app
