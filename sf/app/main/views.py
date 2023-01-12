from flask import Blueprint, render_template, request, session
from flask_login import login_required
from sqlalchemy import func
import datetime


from ..models import Product, ProductOrder, Staff, Shop

from ..calcs import get_amount_today, get_qty_today, get_qty_month, get_amount_month


main = Blueprint('main', __name__)

JST = datetime.timezone(datetime.timedelta(hours=+9), 'JST')
today = datetime.date.today()


# index: sf.furoshiki.in
@main.route('/')
@login_required
def index():

    for key in list(session.keys()):
        session.pop(key)

    page = request.args.get('page', 1, type=int)

    today = datetime.datetime.today()
    a_year_ago = today - datetime.timedelta(days=365)

    filters = [(ProductOrder.date >= a_year_ago)]

    date = request.args.get('date')
    staff = request.args.get('staff')
    shipped = request.args.get('shipped')
    q = request.args.get('q')

    if date:

        session['date'] = date
        filters.append(func.DATE(ProductOrder.date) == date)

    if staff:

        session['staff'] = staff
        filters.append(ProductOrder.sales_by == staff)

    if shipped:

        session['shipped'] = shipped
        filters.append(ProductOrder.shippings != None)

    if q:
        session['q'] = q

        search = f'%{q}%'
        filters.append(ProductOrder.shop.has(Shop.name.like(search)))

    orders = ProductOrder.query.filter(*filters).order_by(ProductOrder.id.desc()).paginate(page=page, per_page=20)

    staffs = Staff.query.filter(Staff.is_inactive==False).all()

    qty_month = get_qty_month()
    amount_month = get_amount_month()
    qty_today = get_qty_today()
    amount_today = get_amount_today()

    return render_template('index.html', orders=orders, page=page, staffs=staffs, qty_today=qty_today,
     amount_today=amount_today, qty_month=qty_month, amount_month=amount_month)


@main.route('/search')
def search():

    page = request.args.get('page', 1, type=int)

    today = datetime.datetime.today()
    a_year_ago = today - datetime.timedelta(days=365)

    filters = [(ProductOrder.date >= a_year_ago)]

    date = request.args.get('date')
    staff = request.args.get('staff')
    shipped = request.args.get('shipped')
    q = request.args.get('q')

    if date:
        filters.append(func.DATE(ProductOrder.date) == date)

    if staff:
        filters.append(ProductOrder.sales_by == staff)

    if shipped:
        filters.append(ProductOrder.shippings != None)

    if q:
        search = f'%{q}%'
        filters.append(ProductOrder.shop.has(Shop.name.like(search)))

    orders = ProductOrder.query.filter(*filters).order_by(ProductOrder.id.desc()).paginate(page=page, per_page=20)

    staffs = Staff.query.filter(Staff.is_inactive==False).all()

    qty_month = get_qty_month()
    amount_month = get_amount_month()
    qty_today = get_qty_today()
    amount_today = get_amount_today()

    return render_template('index.html', orders=orders, page=page, staffs=staffs, qty_today=qty_today,
     amount_today=amount_today, qty_month=qty_month, amount_month=amount_month)


# show products/items list
@main.route('/product')
def product():

    products = Product.query.all()
    return render_template('products.html', products=products)
