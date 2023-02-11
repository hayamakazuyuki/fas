from flask import Blueprint, render_template, request, redirect, url_for, make_response, session
from flask_login import login_required
from io import StringIO
from sqlalchemy import func

from ..models import ProductOrder
from .download import dl_general
from ..calcs import get_total_qty, get_total_amount, get_sum_by_item, get_sum_by_staff, get_orders

import datetime
import csv


downloads = Blueprint('downloads', __name__, url_prefix='/downloads')
JST = datetime.timezone(datetime.timedelta(hours=+9), 'JST')
now = datetime.datetime.now(JST)


@downloads.route('/')
@downloads.route('/<dl>')
@login_required
def index(dl=None):

    target_date = datetime.datetime.now(JST)

    total_qty = get_total_qty(target_date)
    total_amount = get_total_amount(target_date)
    sum_by_item = get_sum_by_item(target_date)
    sum_by_staff = get_sum_by_staff(target_date)

    if dl:
        orders = ProductOrder.query.filter(func.DATE(ProductOrder.date) == func.date(target_date)).all()

        file = StringIO()
        writer = csv.writer(file, lineterminator="\n")
        writer.writerow(
            ['注文番号', '登録日', '営業担当', '顧客ID', '事業所ID', '事業所名', '都道府県', '商品番号', '商品名', '単価', '数量']
            )

        for order in orders:
            writer.writerow([
                order.id, order.date, order.staff.last_name, order.customer_id, order.shop_id, order.shop.name, 
                order.shop.prefecture, order.item, order.product.name, order.price, order.qty
            ])

        response = make_response()
        response.data = file.getvalue().encode('sjis', 'replace')
        response.headers['Content-Type'] = 'text/csv'
        response.headers['Content-Disposition'] = 'attachment; filename=orders-' + target_date.strftime('%Y%m%d-%H%M') + '.csv'

        return response

    return render_template('downloads/index.html', target_date=target_date, total_qty=total_qty,
         total_amount=total_amount, sum_by_item=sum_by_item, sum_by_staff=sum_by_staff)


@downloads.route('/search')
@login_required
def search():

    target_date = request.args.get('targetDate')
    from_date = request.args.get('fromDate')
    to_date = request.args.get('toDate')
    layout = request.args.get('layout')

    total_qty = get_total_qty(target_date, from_date, to_date)
    total_amount = get_total_amount(target_date, from_date, to_date)
    sum_by_item = get_sum_by_item(target_date, from_date, to_date)
    sum_by_staff = get_sum_by_staff(target_date, from_date, to_date)

    orders = get_orders(target_date, from_date, to_date)

    if layout == 'general':

        file = StringIO()
        writer = csv.writer(file, lineterminator="\n")
        writer.writerow(
            ['注文番号', '登録日', '営業担当', '顧客ID', '事業所ID', '事業所名', '都道府県', '商品番号', '商品名', '単価', '数量']
            )

        for order in orders:
            writer.writerow([
                order.id, order.date, order.staff.last_name, order.customer_id, order.shop_id, order.shop.name, 
                order.shop.prefecture, order.item, order.product.name, order.price, order.qty
            ])

        response = make_response()
        response.data = file.getvalue().encode('sjis', 'replace')
        response.headers['Content-Type'] = 'text/csv'
        response.headers['Content-Disposition'] = 'attachment; filename=orders-' + target_date + '.csv'

        return response

    elif layout == 'accounting':

        file = StringIO()
        writer = csv.writer(file, lineterminator="\n")
        writer.writerow(
            ['注文番号', '登録日', '取引先', '事業所', '事業所名', '商品番号', '商品名', '単価', '数量', '出荷日', '出荷場所']
            )

        for order in orders:
            shipped_on = []
            shipped_by = []

            if order.shippings:
                # for date in order.shippings.shipped_on:
                #     shipped_on.append(date)

                # for shipper in order.shippings.registered_by:
                #     shipped_by.append(shipper)
                shipped_on = order.shippings.shipped_on
                shipped_by = order.shippings.registered_by

            else:
                pass
            
            writer.writerow([
                order.id, order.date, order.customer_id, order.shop_id, order.shop.name, 
                order.item, order.product.name, order.price, order.qty, shipped_on, shipped_by
            ])

        response = make_response()
        response.data = file.getvalue().encode('sjis', 'replace')
        response.headers['Content-Type'] = 'text/csv'
        response.headers['Content-Disposition'] = 'attachment; filename=orders-' + now.strftime('%Y-%m-%d') + '.csv'

        return response

    else:
        pass

    return render_template('downloads/searched.html', target_date=target_date, from_date=from_date, to_date=to_date,
         total_qty=total_qty, total_amount=total_amount, sum_by_item=sum_by_item, sum_by_staff=sum_by_staff)
