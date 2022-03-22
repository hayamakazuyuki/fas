from werkzeug.security import generate_password_hash, check_password_hash
from .extentions import db, login_manager
from sqlalchemy import event, func, ForeignKeyConstraint

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


class Parent(db.Model):
    id = db.Column(db.Integer, primary_key=True, auto_increment=True)
    name = db.Column(db.String(100), nullable=False)
    customers = db.relationship('Customer', backref=db.backref('parent', lazy=True))


class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    parent_id = db.Column(db.Integer, db.ForeignKey('parent.id'), nullable=True)
    name = db.Column(db.String(100), nullable=False)
    staff = db.Column(db.Integer, db.ForeignKey('staff.id'), nullable=True)
    shops = db.relationship('Shop', backref=db.backref('customer', lazy=True))


class Shop(db.Model):
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), primary_key=True)
    id = db.Column(db.Integer, primary_key=True)
    shop_number = db.Column(db.String(20), nullable=True)
    name = db.Column(db.String(100), nullable=False)
    department = db.Column(db.String(100))
    zip = db.Column(db.String(7), nullable=False)
    prefecture = db.Column(db.String(4), nullable=False)
    city = db.Column(db.String(30), nullable=False)
    town = db.Column(db.String(30), nullable=False)
    address = db.Column(db.String(50), nullable=False)
    building = db.Column(db.String(50))
    email = db.Column(db.String(100))
    telephone = db.Column(db.String(15), nullable=False)
    is_inactive = db.Column(db.Boolean, nullable=True)
    registered_at = db.Column(db.DateTime, default=func.now())
    orders = db.relationship('ProductOrder', backref=db.backref('shop', lazy=True))


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    abbre = db.Column(db.String(50), nullable=False)
    thickness = db.Column(db.Float)
    qty = db.Column(db.Integer)
    size = db.Column(db.String(100))
    orders = db.relationship('ProductOrder', backref=db.backref('product', lazy=True))
    prices = db.relationship('CustomerPrice', backref=db.backref('product', lazy=True))


class ProductOrder(db.Model):
    __tablename__ = 'product_order'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, default=func.now())
    sales_by = db.Column(db.Integer)
    customer_id = db.Column(db.Integer)
    shop_id = db.Column(db.Integer)
    item = db.Column(db.Integer, db.ForeignKey('product.id'))
    price = db.Column(db.Integer)
    qty = db.Column(db.Integer)
    delivery_check = db.Column(db.Integer, nullable=True)
    exported = db.Column(db.Integer, nullable=True)

    __table_args__ = (ForeignKeyConstraint(['customer_id', 'shop_id'], ['shop.customer_id', 'shop.id']),)


class CustomerPrice(db.Model):
    id = db.Column(db.Integer, primary_key=True, auto_increment=True)
    customer_id = db.Column(db.Integer, nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    price = db.Column(db.Integer, nullable=False)
