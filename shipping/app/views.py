from flask import Blueprint, render_template, request, flash, redirect, url_for, make_response
from flask_login import login_required, current_user
from datetime import datetime, timezone, timedelta, date

from io import StringIO
from sqlalchemy import or_, and_

from .forms import FileUploadForm

import io
import csv

from .models import ProductOrder, DeliveryRequest, Shipping
from .extentions import db


shipping = Blueprint('shipping', __name__)
JST = timezone(timedelta(hours=+9), 'JST')


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
        shipper_code = '0355425300'

        if order.qty == 1 or order.qty >= 5 :

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

            writer.writerow([shipper_code,'','','',order.id,1,3 if order.qty == 1 else 0,order.qty,'','','','','','',''
                ,'','','',order.shop.zip.zfill(7),order.shop.name
                ,order.shop.department,order.shop.prefecture + order.shop.city + order.shop.town + order.shop.address
                ,order.shop.building,order.shop.telephone,'','','',''
                ,'','','','',order.product.name,order.shop.shop_number,memo,'',''
                ,delivery_req, is_request,'','',0])

        elif order.qty >= 2 and order.qty <= 4:
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

            for i in range(order.qty):
                order_id = str(order.id) + '-' + str(i)
                    
                writer.writerow([shipper_code,'','','',order_id,1,3,1,'','','','','','',''
                    ,'','','',order.shop.zip.zfill(7),order.shop.name
                    ,order.shop.department,order.shop.prefecture + order.shop.city + order.shop.town + order.shop.address
                    ,order.shop.building,order.shop.telephone,'','','',''
                    ,'','','','',order.product.name,order.shop.shop_number,memo,'',''
                    ,delivery_req, is_request,'','',0])           

        else:
            pass

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

            # prepare the file name
            filename = 'dl-' + now + '.csv'

            csv_file = prepare_csv(orders, filename)

            if orders:
                for order in orders:
                    order.delivery_check = 2
                db.session.commit()

            return csv_file

    elif shipper == 5808:

        orders = ProductOrder.query.filter(ProductOrder.item != 901)\
            .filter(ProductOrder.product.has(shipper=True)).filter(ProductOrder.delivery_check.is_(None)).all()

        if dl == 'csv':

            # prepare the file name
            filename = 'dl-' + now + '.csv'

            csv_file = prepare_csv(orders, filename)

            if orders:
                for order in orders:
                    order.delivery_check = 1
                db.session.commit()

            return csv_file

    else:
        orders = ProductOrder.query.filter(ProductOrder.item != 901)\
            .filter(ProductOrder.delivery_check.is_(None)).all()

        if dl == 'csv':
            flash('ダウンロードするデータはありません。', 'success')

            redirect(url_for('shipping.index'))

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



ALLOWED_EXTENSIONS = set(['csv'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@shipping.route('/shipped', methods=['GET', 'POST'])
@login_required
def shipped():

    shippings = Shipping.query.order_by(Shipping.id.desc()).all()

    form = FileUploadForm()

    if form.validate_on_submit():

        f = request.files['file']

        if f and allowed_file(f.filename):

            text = io.TextIOWrapper(f)

            reader = csv.reader(text)
            next(reader)

            for row in reader:
                order_id = row[1]

                if not order_id:
                    continue # to next loop

                else:
                    if not '-' in order_id:
                        pass

                    else:
                        idx = order_id.find('-')
                        order_id = order_id[:idx]

                shipping = Shipping(order_id=order_id, shipped_on=row[0], code=row[2])
                db.session.add(shipping)

            db.session.commit()

            flash('出荷データを登録しました。', 'success')
            return redirect(url_for('shipping.shipped'))

    return render_template('shipped.html', form=form, shippings=shippings)
