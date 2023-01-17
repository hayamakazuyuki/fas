import datetime

from sqlalchemy import func, case
from flask_login import current_user
from .extentions import db
from .models import ProductOrder, Product, Staff

JST = datetime.timezone(datetime.timedelta(hours=+9), 'JST')

today = datetime.datetime.now(JST)


def get_amount_today():
    amount_today = db.session.query(func.sum((ProductOrder.price * ProductOrder.qty)))\
        .filter(ProductOrder.sales_by == current_user.id).filter(func.date(ProductOrder.date) == func.date(today)).scalar()

    return amount_today


def get_qty_today():
    qty_today = db.session.query(func.sum(ProductOrder.qty)).filter(ProductOrder.sales_by ==current_user.id)\
        .filter(func.date(ProductOrder.date) == func.date(today)).filter(ProductOrder.item != 901).scalar()

    return qty_today


# ここから
def get_qty_month():
    qty_month = db.session.query(func.sum(ProductOrder.qty)).filter(ProductOrder.sales_by ==current_user.id)\
        .filter(func.date_format(ProductOrder.date, '%Y-%m') == today.strftime('%Y-%m'))\
        .filter(ProductOrder.item != 901).scalar()

    return qty_month


def get_amount_month():
    amount_month = db.session.query(func.sum((ProductOrder.price * ProductOrder.qty)))\
        .filter(ProductOrder.sales_by == current_user.id)\
        .filter(func.date_format(ProductOrder.date, '%Y-%m') == today.strftime('%Y-%m')).scalar()

    return amount_month


def get_total_qty(target_date=None, from_date=None, to_date=None, target_month=None):

    filters = []

    if target_date:
        filters.append(func.date(ProductOrder.date) == func.date(target_date))

    if from_date:
        filters.append(func.date(ProductOrder.date) >= from_date)

    if to_date:
        filters.append(func.date(ProductOrder.date) <= to_date)

    if target_month:
        filters.append(func.date_format(ProductOrder.date, '%Y-%m') == func.date_format(target_month, '%Y-%m'))

    total_qty = db.session.query(func.sum(ProductOrder.qty)).filter(*filters).filter(ProductOrder.item != 901).scalar()

    return total_qty


def get_total_amount(target_date=None, from_date=None, to_date=None, target_month=None):

    filters = []

    if target_date:
        filters.append(func.date(ProductOrder.date) == func.date(target_date))

    if from_date:
        filters.append(func.date(ProductOrder.date) >= from_date)

    if to_date:
        filters.append(func.date(ProductOrder.date) <= to_date)

    if target_month:
        filters.append(func.date_format(ProductOrder.date, '%Y-%m') == func.date_format(target_month, '%Y-%m'))

    total_amount = db.session.query(func.sum((ProductOrder.price * ProductOrder.qty))).filter(*filters).scalar()

    return total_amount


def get_sum_by_item(target_date=None, from_date=None, to_date=None):

    filters = []

    if target_date:
        filters.append(func.date(ProductOrder.date) == func.date(target_date))

    if from_date:
        filters.append(func.date(ProductOrder.date) >= from_date)

    if to_date:
        filters.append(func.date(ProductOrder.date) <= to_date)

    sum_by_item = db.session.query(Product.id, Product.name, Product.abbre, func.sum(ProductOrder.qty), func.sum(ProductOrder.price * ProductOrder.qty))\
        .join(ProductOrder, Product.id == ProductOrder.item).filter(*filters)\
        .group_by(Product.id).order_by(Product.id).all()

    return sum_by_item


def get_sum_by_staff(target_date=None, from_date=None, to_date=None):

    filters = []

    if target_date:
        filters.append(func.date(ProductOrder.date) == func.date(target_date))

    if from_date:
        filters.append(func.date(ProductOrder.date) >= from_date)

    if to_date:
        filters.append(func.date(ProductOrder.date) <= to_date)

    sum_by_staff = db.session.query(Staff.id, Staff.last_name, Staff.first_name,
         func.sum(case([(ProductOrder.item != 901, ProductOrder.qty)], else_=0)),
         func.sum(ProductOrder.price * ProductOrder.qty))\
        .join(ProductOrder, Staff.id == ProductOrder.sales_by).filter(*filters)\
        .group_by(Staff.id).order_by(func.sum(ProductOrder.price * ProductOrder.qty).desc()).all()

    return sum_by_staff


def get_orders(target_date=None, from_date=None, to_date=None):

    filters = []

    if target_date:
        filters.append(func.date(ProductOrder.date) == target_date)

    if from_date:
        filters.append(func.date(ProductOrder.date) >= from_date)

    if to_date:
        filters.append(func.date(ProductOrder.date) <= to_date)

    orders = ProductOrder.query.filter(*filters).all()

    return orders