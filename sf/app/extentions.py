from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_login import LoginManager
from flask_mail import Mail

db = SQLAlchemy()
admin = Admin(template_mode='bootstrap4')
login_manager = LoginManager()
mail = Mail()
