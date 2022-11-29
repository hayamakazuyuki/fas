from flask import Flask
from .extentions import db, admin, login_manager, mail

from .main.views import main
from .customer.views import customer
from .shipping.views import shipping
from .order.views import order
from .staff.views import staff
from .models import MyAdminIndexView


def create_app():
    app = Flask(__name__)
    
    if app.config['ENV'] == 'production':
        app.config.from_object('app.config.ProductionConfig')
    
    elif app.config['ENV'] == 'testing':
        app.config.from_object('app.config.TestingConfig')

    else:
        app.config.from_object('app.config.DevelopmentConfig')

    db.init_app(app)
    admin.init_app(app, index_view=MyAdminIndexView())
    login_manager.init_app(app)
    mail.init_app(app)

    login_manager.login_view = 'staff.login'
    login_manager.login_message = False

    app.register_blueprint(main)
    app.register_blueprint(customer)
    app.register_blueprint(staff)
    app.register_blueprint(shipping)
    app.register_blueprint(order)

    return app
