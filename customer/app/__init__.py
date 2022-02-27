from flask import Flask

from .views import cs
from .extentions import db, login_manager
from .user.views import user

def create_app():
    app = Flask(__name__)

    if app.config['ENV'] == 'production':
        app.config.from_object('app.config.ProductionConfig')
    
    elif app.config['ENV'] == 'testing':
        app.config.from_object('app.config.TestingConfig')

    else:
        app.config.from_object('app.config.DevelopmentConfig')

    db.init_app(app)
    login_manager.init_app(app)

    login_manager.login_message = False


    app.register_blueprint(cs)
    app.register_blueprint(user)
    
    return app