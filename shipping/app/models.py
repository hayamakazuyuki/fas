from werkzeug.security import check_password_hash
from .extentions import db, login_manager
from flask_login import UserMixin
from sqlalchemy import ForeignKeyConstraint, func


class Shipper(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    is_inactive = db.Column(db.Boolean, nullable=True)
    users = db.relationship('ShipperUser', backref=db.backref('shipper', lazy=True))

class ShipperUser(db.Model, UserMixin):
    __tablename__ = 'shipper_user'
    shipper_id = db.Column(db.Integer, db.ForeignKey('shipper.id'), nullable=False)
    id = db.Column(db.Integer, primary_key=True)
    last_name = db.Column(db.String(30), nullable=False)
    first_name = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    is_inactive = db.Column(db.Boolean, nullable=True)

    def check_password(self, password):
        return check_password_hash(self.password, password)


@login_manager.user_loader
def load_user(user_id):
    return ShipperUser.query.get(user_id)
    

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    abbre = db.Column(db.String(50), nullable=False)
    thickness = db.Column(db.Float)
    qty = db.Column(db.Integer)
    size = db.Column(db.String(100))
    shipper = db.Column(db.Boolean, nullable=True)
    orders = db.relationship('ProductOrder', backref=db.backref('product', lazy=True))


class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
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
    orders = db.relationship('ProductOrder', backref=db.backref('shop', lazy=True))


class ProductOrder(db.Model):
    __tablename__ = 'product_order'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime)
    sales_by = db.Column(db.Integer)
    customer_id = db.Column(db.Integer)
    shop_id = db.Column(db.Integer)
    item = db.Column(db.Integer, db.ForeignKey('product.id'))
    price = db.Column(db.Integer)
    qty = db.Column(db.Integer)
    delivery_check = db.Column(db.Integer, nullable=True)
    exported = db.Column(db.Integer, nullable=True)
    request = db.relationship('DeliveryRequest', backref='product_order', uselist=False,
                              cascade="save-update, merge, delete")
    shippings = db.relationship('Shipping', backref='product_order')

    __table_args__ = (ForeignKeyConstraint(['customer_id', 'shop_id'], ['shop.customer_id', 'shop.id']),)


class DeliveryRequest(db.Model):
    __tablename__ = 'delivery_request'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('product_order.id'), nullable=False, unique=True)
    created_at = db.Column(db.DateTime)
    requested_by = db.Column(db.Integer, nullable=False)
    delivery_date = db.Column(db.Date, nullable=True)
    time_range = db.Column(db.String(5), nullable=True)
    memo = db.Column(db.String(255), nullable=True)
    checked = db.Column(db.Integer, nullable=True)


class Shipping(db.Model):
    id = db.Column(db.Integer, primary_key=True, auto_increment=True)
    order_id = db.Column(db.Integer, db.ForeignKey('product_order.id'), nullable=False)
    shipped_on = db.Column(db.Date, nullable=False)
    code = db.Column(db.String(15), nullable=False, unique=True)
    registered_at = db.Column(db.DateTime, default=func.now())
    registered_by = db.Column(db.String(255), nullable=False)
