import datetime

from sqlalchemy import func
from .extentions import db
from .models import Product, ProductOrder, Shipping

JST = datetime.timezone(datetime.timedelta(hours=+9), 'JST')
today = datetime.datetime.now(JST)


def get_shipped_items(today):

    shipped_items = db.session.query(Product.id, Product.name, func.sum(ProductOrder.qty))\
        .join(ProductOrder, Product.id == ProductOrder.item)\
        .group_by(Product.id).order_by(Product.id).all()

    return shipped_items
