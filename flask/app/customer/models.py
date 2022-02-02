from ..extentions import db

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    shops = db.relationship('Shop', backref=db.backref('customer', lazy=True))


class Shop(db.Model):
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), primary_key=True)
    id = db.Column(db.Integer, primary_key=True)
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
    # orders = db.relationship('PurchaseOrder', backref=db.backref('shop', lazy=True))