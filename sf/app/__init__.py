from flask import Flask
from .extentions import db, admin, login_manager

from .main.views import main
from .customer.views import customer
from .delivery.views import delivery
from .order.views import order
from .staff.views import staff


def create_app(config_file='settings.py'):
    app = Flask(__name__)
    
    app.config.from_pyfile(config_file)

    db.init_app(app)
    admin.init_app(app)
    login_manager.init_app(app)
    
    login_manager.login_view = 'staff.login'
    login_manager.login_message = False

    app.register_blueprint(main)
    app.register_blueprint(customer)
    app.register_blueprint(staff)
    app.register_blueprint(delivery)
    app.register_blueprint(order)

    return app
