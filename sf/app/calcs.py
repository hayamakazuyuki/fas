import datetime

from sqlalchemy import func
from flask_login import current_user
from .extentions import db
from .models import ProductOrder

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


def get_total_qty_today():
    total_qty_today = db.session.query(func.sum(ProductOrder.qty))\
        .filter(func.date(ProductOrder.date) == func.date(today)).filter(ProductOrder.item != 901).scalar()

    return total_qty_today


def get_total_amount_today():
    total_amount_today = db.session.query(func.sum((ProductOrder.price * ProductOrder.qty)))\
        .filter(func.date(ProductOrder.date) == func.date(today)).scalar()

    return total_amount_today
