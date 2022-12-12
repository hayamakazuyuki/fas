from flask import Blueprint, render_template, request, make_response, session, redirect, url_for
from flask_login import current_user, login_required
from sqlalchemy import extract, func, or_, and_
from io import StringIO
import csv
import datetime

from ..email import send_email

from ..models import Product, ProductOrder, Staff, Shop

from app import db


main = Blueprint('main', __name__)
JST = datetime.timezone(datetime.timedelta(hours=+9), 'JST')

this_year  = datetime.datetime.now(JST).strftime('%Y')
this_month = datetime.datetime.now(JST).strftime('%m')
today = datetime.date.today()


def get_my_qty_month():
    my_qty_month = db.session.query(func.sum(ProductOrder.qty)).filter(ProductOrder.sales_by ==current_user.id)\
        .filter(extract('year', ProductOrder.date) == this_year).filter(extract('month', ProductOrder.date) == this_month)\
        .filter(ProductOrder.item != 901).scalar()
    return my_qty_month


def get_my_amount_month():
    my_amount_month = db.session.query(func.sum((ProductOrder.price * ProductOrder.qty)))\
        .filter(ProductOrder.sales_by == current_user.id)\
        .filter(extract('year', ProductOrder.date) == this_year).filter(extract('month', ProductOrder.date) == this_month)\
        .scalar()
    return my_amount_month


def get_my_qty_today():
    my_qty_today = db.session.query(func.sum(ProductOrder.qty)).filter(ProductOrder.sales_by ==current_user.id)\
        .filter(func.date(ProductOrder.date) == today).filter(ProductOrder.item != 901).scalar()
    return my_qty_today


def get_my_amount_today():
    my_amount_today = db.session.query(func.sum((ProductOrder.price * ProductOrder.qty)))\
        .filter(ProductOrder.sales_by == current_user.id).filter(func.date(ProductOrder.date) == today).scalar()
    return my_amount_today


def get_total_qty_today():
    total_qty_today = db.session.query(func.sum(ProductOrder.qty))\
        .filter(func.date(ProductOrder.date) == today).filter(ProductOrder.item != 901).scalar()
    return total_qty_today


def get_total_amount_today():
    total_amount_today = db.session.query(func.sum((ProductOrder.price * ProductOrder.qty)))\
        .filter(func.date(ProductOrder.date) == today).scalar()
    return total_amount_today



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

    # orders = ProductOrder.query.filter(func.DATE(ProductOrder.date) == date)\
    #     .filter_by(sales_by=staff)\
    #         .order_by(ProductOrder.id.desc()).paginate(page=page, per_page=20)

    # this_year  = datetime.datetime.now(JST).strftime('%Y')
    # this_month = datetime.datetime.now(JST).strftime('%m')
    # today = datetime.date.today()

    my_qty_month = get_my_qty_month()
    my_amount_month = get_my_amount_month()
    my_qty_today = get_my_qty_today()
    my_amount_today = get_my_amount_today()
    total_qty_today = get_total_qty_today()
    total_amount_today = get_total_amount_today()

    # my_qty_month = db.session.query(func.sum(ProductOrder.qty)).filter(ProductOrder.sales_by ==current_user.id)\
    #     .filter(extract('year', ProductOrder.date) == this_year).filter(extract('month', ProductOrder.date) == this_month)\
    #     .filter(ProductOrder.item != 901).scalar()

    # my_amount_month = db.session.query(func.sum((ProductOrder.price * ProductOrder.qty)))\
    #     .filter(ProductOrder.sales_by == current_user.id)\
    #     .filter(extract('year', ProductOrder.date) == this_year).filter(extract('month', ProductOrder.date) == this_month)\
    #     .scalar()

    # my_qty_today = db.session.query(func.sum(ProductOrder.qty)).filter(ProductOrder.sales_by ==current_user.id)\
    #     .filter(func.date(ProductOrder.date) == today).filter(ProductOrder.item != 901).scalar()

    # my_amount_today = db.session.query(func.sum((ProductOrder.price * ProductOrder.qty)))\
    #     .filter(ProductOrder.sales_by == current_user.id).filter(func.date(ProductOrder.date) == today).scalar()

    # total_qty_today = db.session.query(func.sum(ProductOrder.qty))\
    #     .filter(func.date(ProductOrder.date) == today).filter(ProductOrder.item != 901).scalar()

    # total_amount_today = db.session.query(func.sum((ProductOrder.price * ProductOrder.qty)))\
    #     .filter(func.date(ProductOrder.date) == today).scalar()

    return render_template('index.html', orders=orders, page=page, staffs=staffs, my_qty_today=my_qty_today,
     my_amount_today=my_amount_today, my_qty_month=my_qty_month, my_amount_month=my_amount_month, total_qty_today=total_qty_today,
     total_amount_today=total_amount_today)

    # today = datetime.now(JST).strftime('%Y-%m-%d')

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

    my_qty_month = get_my_qty_month()
    my_amount_month = get_my_amount_month()
    my_qty_today = get_my_qty_today()
    my_amount_today = get_my_amount_today()
    total_qty_today = get_total_qty_today()
    total_amount_today = get_total_amount_today()

    return render_template('index.html', orders=orders, page=page, staffs=staffs, my_qty_today=my_qty_today,
     my_amount_today=my_amount_today, my_qty_month=my_qty_month, my_amount_month=my_amount_month, total_qty_today=total_qty_today,
     total_amount_today=total_amount_today)


# @main.route('/drop-session')
# def drop_session():

#     for key in list(session.keys()):
#         session.pop(key)

#     return redirect(url_for('main.index'))


# show products/items list
@main.route('/product')
def product():

    products = Product.query.all()
    return render_template('products.html', products=products)


def prepare_csv(orders, filename):
    file = StringIO()
    writer = csv.writer(file, lineterminator="\n")

    writer.writerow(['荷送人コード','西濃発店コード','出荷予定日','お問合番号','管理番号','元着区分','原票区分'
                    ,'個数','重量区分','重量K','重量才','荷送人名称','荷送人住所','荷送人住所2','荷送人電話番号'
                    ,'部署コード','部署名','重量契約区分','お届先郵便番号','お届先名称','お届先名称2','お届先住所'
                    ,'お届先住所2','お届先電話番号','お届先コード','お届先JIS市町村','着店コード付け区分','着地コード'
                    ,'着店コード','保険金額','輸送指示1','輸送指示2','記事1','記事2','記事3','記事4','記事5'
                    ,'輸送指示','輸送指示コード1','輸送指示コード2','輸送指示止め店','予備'])

    for order in orders:
        is_request = ''
        memo = ''
        delivery_req = ''

        if order.request is None:
            pass

        else:
            req_date = order.request.delivery_date
            req_time = order.request.time_range

            if req_date and req_time:
                date = req_date.strftime('%m%d')
                delivery_req = date + req_time

            elif req_date and not req_time:
                date = req_date.strftime('%m%d')
                delivery_req = date + '0'

            elif not req_date and req_time:
                delivery_req = '0000' + req_time

            if order.request.delivery_date or order.request.time_range:
                is_request = '02'

            if order.request.memo:
                memo = order.request.memo

            else:
                pass

        writer.writerow(['','','','',order.id,1,0,order.qty,'','','','','','',''
            ,'','','',order.shop.zip.zfill(7),order.shop.name
            ,order.shop.department,order.shop.prefecture + order.shop.city + order.shop.town + order.shop.address
            ,order.shop.building,order.shop.telephone,'','','',''
            ,'','','','',order.product.name,order.shop.shop_number,memo,'',''
            ,delivery_req, is_request,'','',0])

    response = make_response()
    response.data = file.getvalue().encode('sjis', 'replace')
    response.headers['Content-Type'] = 'text/csv'
    response.headers['Content-Disposition'] = 'attachment; filename=' + filename

    return response

# @main.route('/mock')
# def mock():
#     return render_template('mock.html')

@main.route('/test')
def test():

    orders = ProductOrder.query.filter(ProductOrder.item != 901)\
        .filter(or_(ProductOrder.delivery_check ==2, and_(ProductOrder.product.has(shipper=True), ProductOrder.delivery_check.is_(None)))).all()

    # prepare the file name
    filename = 'dl-' + now + '.csv'

    prepare_csv(orders, filename)

    send_email('ライプロンDLデータ')

    # if orders:
    #     for order in orders:
    #         order.delivery_check = 1
    #     db.session.commit()

    return '完了'

# @main.route('/args')
# def args():
#     date = request.args.get('date')

#     if date:

#         return f'{date}'

#     else:
#         return 'なし'