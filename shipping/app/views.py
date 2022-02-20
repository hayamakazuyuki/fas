from operator import or_
from flask import Blueprint, render_template, request, flash, redirect, url_for, make_response
from flask_login import login_required, current_user
from datetime import datetime, timezone, timedelta
from io import StringIO
from sqlalchemy import or_

import csv

from .models import Order, DeliveryRequest
from .extentions import db
from .email import send_email

shipping = Blueprint('shipping', __name__)
JST = timezone(timedelta(hours=+9), 'JST')


@shipping.route('/')
@shipping.route('/<string:dl>')
@login_required
def index(dl=None):

    now = datetime.now(JST).strftime('%Y%m%d-%H%M')
    shipper = current_user.shipper_id

    # get orders
    if shipper == 5388:
        orders = Order.query.filter(Order.item != 901)\
            .filter(Order.item != 602).filter(Order.item != 603).filter(Order.item != 604)\
            .filter(Order.item != 622).filter(Order.item != 642).filter(Order.item != 680)\
            .filter(Order.delivery_check.is_(None)).all()
        
        if dl == 'csv':
            file = StringIO()
            writer = csv.writer(file, lineterminator="\n")

            writer.writerow(['荷受人コード', '電話番号', 'FAX番号', '住所1', '住所2', '住所3', '名前1', '名前2', '予約', '郵便番号',
                         'カナ略称', '一斉出荷区分', '特殊計', '着店コード', '商品（色）', '商品数'])
            for order in orders:
                writer.writerow(['', order.shop_orders.telephone, '', order.shop_orders.prefecture + order.shop_orders.city,
                        order.shop_orders.town + order.shop_orders.address, order.shop_orders.building,
                        order.shop_orders.name, order.shop_orders.department, '',
                        f"{order.shop_orders.zip[:3]}-{order.shop_orders.zip[3:]}",
                        '', '', '', '', order.product_orders.name, order.qty])

            # prepare the file name
            filename = 'dl-' + now + '.csv'

            # prepare DL data
            response = make_response()
            response.data = file.getvalue().encode('sjis', 'replace')
            response.headers['Content-Type'] = 'text/csv'
            response.headers['Content-Disposition'] = 'attachment; filename=' + filename

            if orders:
                for order in orders:
                    order.delivery_check = 2
                db.session.commit()

            return response

    elif shipper == 9999:
        orders = Order.query.filter(Order.item != 901).filter(or_(Order.delivery_check != 1, Order.delivery_check.is_(None))).all()

        if dl == 'csv':
            file = StringIO()
            writer = csv.writer(file, lineterminator="\n")

            writer.writerow(['荷受人コード', '電話番号', 'FAX番号', '住所1', '住所2', '住所3', '名前1', '名前2', '予約', '郵便番号',
                         'カナ略称', '一斉出荷区分', '特殊計', '着店コード', '商品（色）', '商品数'])
            for order in orders:
                writer.writerow(['', order.shop_orders.telephone, '', order.shop_orders.prefecture + order.shop_orders.city,
                        order.shop_orders.town + order.shop_orders.address, order.shop_orders.building,
                        order.shop_orders.name, order.shop_orders.department, '',
                        f"{order.shop_orders.zip[:3]}-{order.shop_orders.zip[3:]}",
                        '', '', '', '', order.product_orders.name, order.qty])

            # prepare the file name
            filename = 'dl-' + now + '.csv'

            # prepare DL data
            response = make_response()
            response.data = file.getvalue().encode('sjis', 'replace')
            response.headers['Content-Type'] = 'text/csv'
            response.headers['Content-Disposition'] = 'attachment; filename=' + filename

            if orders:
                for order in orders:
                    order.delivery_check = 1
                db.session.commit()

            return response

    else:
        orders = ''

        # email attachment to sf
        # attachment = file.getvalue().encode('sjis', 'replace')
        # send_email('test ライプロンDLデータ', recipients=['hayama@sfinter.com'], body='ライプロンのダウンロードデータです。',
        #            filename=filename, attachment=attachment)

    return render_template('index.html', orders=orders, now=now)


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

# @shipping.route('/now')
# def now():

#     now = datetime.now(JST).strftime('%Y%m%d-%H%M')

#     return now


# @shipping.route('/conf')
# def conf():
#     return current_app.config['SECRET_KEY']
