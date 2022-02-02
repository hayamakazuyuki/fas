from .extentions import db, admin
from flask_admin import AdminIndexView
from flask_admin.contrib.sqla import ModelView

from sqlalchemy import ForeignKeyConstraint, func

from datetime import datetime, timedelta, timezone

JST = timezone(timedelta(hours=+9), 'JST')


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    thickness = db.Column(db.Float)
    qty = db.Column(db.Integer)
    size = db.Column(db.String(100))
    box_size = db.Column(db.String(100))
    # orders = db.relationship('PurchaseOrder', backref=db.backref('product', lazy=True))






# class PurchaseOrder(db.Model):
#     __tablename__ = 'purchase_order'
#     id = db.Column(db.Integer, primary_key=True)
#     date = db.Column(db.DateTime, default=func.now(JST))
#     sales_by = db.Column(db.Integer, db.ForeignKey('user.id'))
#     customer_id = db.Column(db.Integer)
#     shop_id = db.Column(db.Integer)
#     item = db.Column(db.Integer, db.ForeignKey('product.id'))
#     price = db.Column(db.Integer)
#     qty = db.Column(db.Integer)
#     delivery_check = db.Column(db.Integer, nullable=True)
#     exported = db.Column(db.Integer, nullable=True)
#     request = db.relationship('DeliveryRequest', backref='purchase_order', uselist=False,
#                               cascade="save-update, merge, delete")

#     __table_args__ = (ForeignKeyConstraint(['customer_id', 'shop_id'], ['shop.customer_id', 'shop.id']),)


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


class ProductAdminView(ModelView):
    form_columns = ['id', 'name', 'thickness', 'qty', 'size', 'box_size']
    column_list = ['id', 'name', 'thickness', 'qty', 'size', 'box_size']


admin.add_view(ProductAdminView(Product, db.session))
