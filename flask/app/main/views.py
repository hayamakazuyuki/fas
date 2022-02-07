from datetime import datetime, timedelta, timezone, date
from flask import Blueprint, render_template, request
from flask_login import current_user, login_required
from sqlalchemy import func

from ..models import Product, ProductOrder

from app import db

main = Blueprint('main', __name__)
JST = timezone(timedelta(hours=+9), 'JST')


# index: sf.furoshiki.in
@main.route('/')
@login_required
def index():
    page = request.args.get('page', 1, type=int)
    orders = ProductOrder.query.filter(ProductOrder.sales_by == current_user.id).order_by(ProductOrder.id.desc()).paginate(page=page, per_page=20)
    # today = date.today()
    today = datetime.now(JST).strftime('%Y-%m-%d')

    sum_qty_today = db.session.query(func.sum(ProductOrder.qty)).filter(ProductOrder.sales_by ==current_user.id)\
        .filter(func.date(ProductOrder.date) == today).filter(ProductOrder.item != 901).scalar()

    sum_amount_today = db.session.query(func.sum((ProductOrder.price * ProductOrder.qty)))\
        .filter(ProductOrder.sales_by == current_user.id).filter(func.date(ProductOrder.date) == today).scalar()

    return render_template('index.html', orders=orders, today=today, sum_qty_today=sum_qty_today, sum_amount_today=sum_amount_today)


# show products/items list
@main.route('/product')
def product():

    products = Product.query.all()
    return render_template('products.html', products=products)

