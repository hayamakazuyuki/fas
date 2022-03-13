from email.policy import default
from werkzeug.security import generate_password_hash, check_password_hash
from .extentions import db, admin, login_manager
from flask_admin import AdminIndexView
from flask_admin.contrib.sqla import ModelView

from flask_login import UserMixin
from sqlalchemy import ForeignKeyConstraint, func, event, true, UniqueConstraint

from datetime import datetime, timedelta, timezone

JST = timezone(timedelta(hours=+9), 'JST')


class Staff(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    last_name = db.Column(db.String(30), nullable=False)
    first_name = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    is_inactive = db.Column(db.Boolean, nullable=True)
    orders = db.relationship('ProductOrder', backref=db.backref('staff', lazy=True))
    customers = db.relationship('Customer', backref=db.backref('sales', lazy=True))

    def check_password(self, password):
        return check_password_hash(self.password, password)


@event.listens_for(Staff.password, 'set', retval=True)
def hash_staff_password(target, value, oldvalue, initiator):
    if value != oldvalue:
        return generate_password_hash(value)
    return value


@login_manager.user_loader
def load_user(user_id):
    return Staff.query.get(int(user_id))


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    abbre = db.Column(db.String(50), nullable=False)
    thickness = db.Column(db.Float)
    qty = db.Column(db.Integer)
    size = db.Column(db.String(100))
    shipper = db.Column(db.Boolean, nullable=True, default=0)
    orders = db.relationship('ProductOrder', backref=db.backref('product', lazy=True))


class Parent(db.Model):
    id = db.Column(db.Integer, primary_key=True, auto_increment=True)
    name = db.Column(db.String(100), nullable=False)
    customers = db.relationship('Customer', backref=db.backref('parent', lazy=True))


class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    parent_id = db.Column(db.Integer, db.ForeignKey('parent.id'), nullable=True)
    name = db.Column(db.String(100), nullable=False)
    staff = db.Column(db.Integer, db.ForeignKey('staff.id'), nullable=True)
    registered_at = db.Column(db.DateTime, default=func.now())
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


class ProductOrder(db.Model):
    __tablename__ = 'product_order'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, default=func.now())
    sales_by = db.Column(db.Integer, db.ForeignKey('staff.id'))
    customer_id = db.Column(db.Integer)
    shop_id = db.Column(db.Integer)
    item = db.Column(db.Integer, db.ForeignKey('product.id'))
    price = db.Column(db.Integer)
    qty = db.Column(db.Integer)
    delivery_check = db.Column(db.Integer, nullable=True)
    exported = db.Column(db.Integer, nullable=True)
    request = db.relationship('DeliveryRequest', backref='product_order', uselist=False,
                              cascade="save-update, merge, delete")

    __table_args__ = (ForeignKeyConstraint(['customer_id', 'shop_id'], ['shop.customer_id', 'shop.id']),)


class CustomerPrice(db.Model):
    id = db.Column(db.Integer, primary_key=True, auto_increment=True)
    customer_id = db.Column(db.Integer, nullable=False)
    product_id = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    __table_args__ = (
        db.UniqueConstraint('customer_id', 'product_id'),
    )

class DeliveryRequest(db.Model):
    __tablename__ = 'delivery_request'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('product_order.id'), nullable=False, unique=True)
    created_at = db.Column(db.DateTime, default=datetime.now(JST))
    requested_by = db.Column(db.Integer, nullable=False)
    delivery_date = db.Column(db.Date, nullable=True)
    time_range = db.Column(db.String(5), nullable=True)
    memo = db.Column(db.String(255), nullable=True)
    reply = db.Column(db.String(255), nullable=True)
    checked = db.Column(db.Integer, nullable=True)


class Shipper(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    is_inactive = db.Column(db.Boolean, nullable=True)
    users = db.relationship('ShipperUser', backref=db.backref('shipper', lazy=True))

class ShipperAdminView(ModelView):
    form_columns = ['id', 'name', 'is_inactive']
    column_list = ['id', 'name', 'is_inactive']


class ShipperUser(db.Model):
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


@event.listens_for(ShipperUser.password, 'set', retval=True)
def hash_staff_password(target, value, oldvalue, initiator):
    if value != oldvalue:
        return generate_password_hash(value)
    return value


class CustomerUser(db.Model):
    __tablename__ = 'customer_user'
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, nullable=False)
    shop_id = db.Column(db.Integer, nullable=True)
    last_name = db.Column(db.String(30), nullable=True)
    first_name = db.Column(db.String(30), nullable=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    is_hq = db.Column(db.Boolean, nullable=True)
    is_inactive = db.Column(db.Boolean, nullable=True)

    def check_password(self, password):
        return check_password_hash(self.password, password)


@event.listens_for(CustomerUser.password, 'set', retval=True)
def hash_staff_password(target, value, oldvalue, initiator):
    if value != oldvalue:
        return generate_password_hash(value)
    return value

class CustomerAdminView(ModelView):
    form_excluded_columns = ['shops', 'registered_at']

class ShopAdminView(ModelView):
    form_excluded_columns = ['orders', 'registered_at']

class StaffAdminView(ModelView):
    form_excluded_columns = ['orders']

class ProductAdminView(ModelView):
    form_columns = ['id', 'name', 'abbre', 'thickness', 'qty', 'size', 'shipper']
    form_excluded_columns = ['orders']

class DisplayProductView(ModelView):
    form_columns = ['id', 'name']
    column_list = ['id', 'name']


admin.add_view(CustomerAdminView(Customer, db.session, endpoint="customerview"))
admin.add_view(ShopAdminView(Shop, db.session))
admin.add_view(ModelView(CustomerPrice, db.session))
admin.add_view(StaffAdminView(Staff, db.session, endpoint="staffview"))
admin.add_view(ProductAdminView(Product, db.session))
admin.add_view(ModelView(Parent, db.session))
admin.add_view(ModelView(ProductOrder, db.session))

admin.add_view(ShipperAdminView(Shipper,db.session))
admin.add_view(ModelView(ShipperUser, db.session))

admin.add_view(ModelView(CustomerUser, db.session))


