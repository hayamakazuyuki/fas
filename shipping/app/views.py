from operator import or_
from flask import Blueprint, render_template, request, flash, redirect, url_for, make_response
from flask_login import login_required, current_user
from datetime import datetime, timezone, timedelta
from io import StringIO
from sqlalchemy import or_, and_

import csv

from .models import ProductOrder, DeliveryRequest
from .extentions import db


shipping = Blueprint('shipping', __name__)
JST = timezone(timedelta(hours=+9), 'JST')


def prepare_csv(orders, now):
    file = StringIO()
    writer = csv.writer(file, lineterminator="\n")

    writer.writerow(['荷受人コード', '電話番号', 'FAX番号', '住所1', '住所2', '住所3', '名前1', '名前2', '予約', '郵便番号',
                         'カナ略称', '一斉出荷区分', '特殊計', '着店コード', '商品（色）', '商品数'])
    for order in orders:
        writer.writerow(['', order.shop.telephone, '', order.shop.prefecture + order.shop.city,
                    order.shop.town + order.shop.address, order.shop.building,
                    order.shop.name, order.shop.department, '',
                    f"{order.shop.zip[:3]}-{order.shop.zip[3:]}",
                    '', '', '', '', order.product.name, order.qty])

    # prepare the file name
    filename = 'dl-' + now + '.csv'

    response = make_response()
    response.data = file.getvalue().encode('sjis', 'replace')
    response.headers['Content-Type'] = 'text/csv'
    response.headers['Content-Disposition'] = 'attachment; filename=' + filename

    return response


@shipping.route('/')
@shipping.route('/<string:dl>')
@login_required
def index(dl=None):

    now = datetime.now(JST).strftime('%Y%m%d-%H%M')
    shipper = current_user.shipper_id

    # get orders
    if shipper == 5388:
        orders = ProductOrder.query.filter(ProductOrder.item != 901)\
            .filter(ProductOrder.product.has(shipper=False)).filter(ProductOrder.delivery_check.is_(None)).all()
        
        if dl == 'csv':

            csv_file = prepare_csv(orders, now)

            if orders:
                for order in orders:
                    order.delivery_check = 2
                db.session.commit()

            return csv_file

    elif shipper == 9999:
        orders = ProductOrder.query.filter(ProductOrder.item != 901)\
            .filter(or_(ProductOrder.delivery_check ==2, and_(ProductOrder.product.has(shipper=True), ProductOrder.delivery_check.is_(None)))).all()

        if dl == 'csv':

            csv_file = prepare_csv(orders, now)

            if orders:
                for order in orders:
                    order.delivery_check = 1
                db.session.commit()

            return csv_file

    else:
        orders = ''

    return render_template('index.html', orders=orders)


@shipping.route('/requests', methods=['GET', 'POST'])
@login_required
def requests():

    requests = DeliveryRequest.query.filter(DeliveryRequest.checked.is_(None)).order_by(DeliveryRequest.id.desc()).all()

    if request.method == 'POST':
        id = request.form['request_id']
        target_request = DeliveryRequest.query.get(id)
        target_request.checked = 1
        db.session.commit()

        flash('1件非表示にしました。')
        return redirect(url_for('shipping.requests'))

    return render_template('requests.html', requests=requests)


@shipping.route('/request_detail/<int:id>', methods=['GET', 'POST'])
@login_required
def request_detail(id):

    delivery_request = DeliveryRequest.query.get(id)

    if request.method == 'POST':
        delivery_request.reply = request.form['reply']
        db.session.commit()

        flash('回答を登録しました。', 'success')
        return redirect(url_for('shipping.requests'))

    return render_template('request-detail.html', delivery_request=delivery_request)


@shipping.route('/count')
@login_required
def count():
    orders = ProductOrder.query.filter(ProductOrder.item != 901).filter(ProductOrder.delivery_check == 2).all()

    count = len(orders)
    return str(count)


# @shipping.route('/change')
# @login_required
# def change():
    
#     orders = Order.query.filter(Order.item != 901).filter(Order.delivery_check == 2).all()

#     for order in orders:
#         order.delivery_check = 1
#     db.session.commit()

#     return redirect(url_for('shipping.count'))



# @shipping.route('/now')
# def now():

#     now = datetime.now(JST).strftime('%Y%m%d-%H%M')

#     return now


# @shipping.route('/conf')
# def conf():
#     return current_app.config['SECRET_KEY']
