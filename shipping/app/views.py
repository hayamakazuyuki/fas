from flask import Blueprint, render_template, request, flash, redirect, url_for, make_response
from datetime import datetime, timezone, timedelta
from io import StringIO
import csv

from .models import Order, DeliveryRequest
from .extentions import db
from .email import send_email


shipping = Blueprint('shipping', __name__)
JST = timezone(timedelta(hours=+9), 'JST')


@shipping.route('/')
@shipping.route('/home')
def index():

    dl = request.args.get("dl")

    if dl == 'csv':  # csvダウンロードがクリックされた時の実行
        now = datetime.now(JST)
        str_now = now.strftime('%Y%m%d-%H%M')

        file = StringIO()
        writer = csv.writer(file, lineterminator="\n")
        orders = Order.query.filter(Order.item != 901).filter(Order.delivery_check.is_(None)).all()

        writer.writerow(['荷受人コード', '電話番号', 'FAX番号', '住所1', '住所2', '住所3', '名前1', '名前2', '予約', '郵便番号',
                         'カナ略称', '一斉出荷区分', '特殊計', '着店コード', '商品（色）', '商品数'])
        for order in orders:
            writer.writerow(['', order.shop_orders.telephone, '', order.shop_orders.prefecture + order.shop_orders.city,
                             order.shop_orders.town + order.shop_orders.address, order.shop_orders.building,
                             order.shop_orders.name, order.shop_orders.department, '',
                             f"{order.shop_orders.zip[:3]}-{order.shop_orders.zip[3:]}",
                             '', '', '', '', order.product_orders.name, order.qty])

        # prepare the file name
        filename = 'dl-' + str_now + '.csv'

        # email attachment to sf
        attachment = file.getvalue().encode('sjis', 'replace')
        send_email('ライプロンのDLデータ', recipients=['hayama@sfinter.com'], body='ライプロンのダウンロードデータです。',
                   filename=filename, attachment=attachment)

        # prepare DL data for ripe lawn
        response = make_response()
        response.data = file.getvalue().encode('sjis', 'replace')
        response.headers['Content-Type'] = 'text/csv'
        response.headers['Content-Disposition'] = 'attachment; filename=' + filename

        return response

    # when accessed to index
    orders = Order.query.filter(Order.item != 901).filter(Order.delivery_check.is_(None)).all()
    return render_template('index.html', orders=orders, now=datetime.now(JST))


@shipping.route('/requests', methods=['GET', 'POST'])
def requests():

    requests = DeliveryRequest.query.filter(DeliveryRequest.checked.is_(None)).order_by(DeliveryRequest.id.desc()).all()

    if request.method == 'POST':
        id = request.form['request_id']
        target_request = DeliveryRequest.query.get(id)
        target_request.checked = 1
        db.session.commit()

        flash('1件非表示にしました。')
        return redirect(url_for('requests'))

    return render_template('requests.html', requests=requests)


@shipping.route('/request_detail/<int:id>', methods=['GET', 'POST'])
def request_detail(id):

    delivery_request = DeliveryRequest.query.get(id)

    if request.method == 'POST':
        delivery_request.reply = request.form['reply']
        db.session.commit()

        flash('回答を登録しました。', 'success')
        return redirect(url_for('shipping.requests'))

    return render_template('request-detail.html', delivery_request=delivery_request)
