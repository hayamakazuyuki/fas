from werkzeug.security import generate_password_hash, check_password_hash
from .extentions import db, login_manager
from sqlalchemy import event, func

from flask_login import UserMixin

from datetime import datetime,timedelta,timezone

JST = timezone(timedelta(hours=+9), 'JST')


class CustomerUser(db.Model, UserMixin):
    __tablename__ = 'customer_user'
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    shop_id = db.Column(db.Integer, nullable=True)
    last_name = db.Column(db.String(30), nullable=False)
    first_name = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    is_hq = db.Column(db.Boolean, nullable=True)
    is_inactive = db.Column(db.Boolean, nullable=True)
    registered_at = db.Column(db.DateTime, default=func.now())

    def check_password(self, password):
        return check_password_hash(self.password, password)


@event.listens_for(CustomerUser.password, 'set', retval=True)
def hash_staff_password(target, value, oldvalue, initiator):
    if value != oldvalue:
        return generate_password_hash(value)
    return value

@login_manager.user_loader
def load_user(user_id):
    return CustomerUser.query.get(int(user_id))