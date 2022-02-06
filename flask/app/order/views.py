from crypt import methods
from datetime import datetime, timezone, timedelta
from flask import Blueprint, render_template, request, redirect, url_for, make_response
from flask_login import current_user, login_required
from sqlalchemy import func
from io import StringIO
import csv

from ..extentions import db

from ..models import Shop, ProductOrder


order = Blueprint('order', __name__, url_prefix='/order')

JST = timezone(timedelta(hours=+9), 'JST')

@order.route('/', methods=['GET', 'POST'])
@login_required
def index():

    customer_id = request.args.get('customer_id')
    id = request.args.get('id')
    
    shop = Shop.query.get((customer_id, id))

    if request.method == 'POST':

        staff = current_user.id
        customer_id = request.form['customer_id']
        id = request.form['id']

        item2 = request.form.get('item2')
        item3 = request.form.get('item3')
        delivery = request.form.get('delivery')

        # item 1
        order = ProductOrder()
        order.sales_by = staff
        order.customer_id = customer_id
        order.shop_id = id
        order.item = request.form['item']
        order.price = request.form['price']
        order.qty = request.form['qty']
        order.delivery_check = request.form.get('noDelivery')

        db.session.add(order)

        if item2:
            order2 = ProductOrder()
            order2.sales_by = staff
            order2.customer_id = customer_id
            order2.shop_id = id
            order2.item = request.form['item2']
            order2.price = request.form['price2']
            order2.qty = request.form['qty2']
            order2.delivery_check = request.form.get('noDelivery2')

            db.session.add(order2)

        if item3:
            order3 = ProductOrder()
            order3.sales_by = staff
            order3.customer_id = customer_id
            order3.shop_id = id
            order3.item = request.form['item3']
            order3.price = request.form['price3']
            order3.qty = request.form['qty3']
            order3.delivery_check = request.form.get('noDelivery3')

            db.session.add(order3)

        if delivery:
            orderd = ProductOrder()
            orderd.sales_by = staff
            orderd.customer_id = customer_id
            orderd.shop_id = id
            orderd.item = request.form['delivery']
            orderd.price = request.form['deliveryPrice']
            orderd.qty = request.form['deliveryQty']

            db.session.add(orderd)

        db.session.commit()

        return redirect(url_for('customer.index'))

    return render_template('order/register.html', shop=shop)


@order.route('/data')
@login_required
def data():
    target = request.args.get("target")
    dl = request.args.get('dl')

    if target is None:
        today = datetime.now(JST)
        target = today.strftime('%Y-%m-%d')

    orders = ProductOrder.query.filter(func.DATE(ProductOrder.date) == target).all()

    if dl == 'csv':
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
        response.headers['Content-Disposition'] = 'attachment; filename=orders-' + target + '.csv'
        return response

    sum_qty = db.session.query(func.sum(ProductOrder.qty)).filter(func.date(ProductOrder.date) == target)\
        .filter(ProductOrder.item != 901).scalar()
    sum_price = db.session.query(func.sum(ProductOrder.price * ProductOrder.qty))\
        .filter(func.date(ProductOrder.date) == target).filter(ProductOrder.item != 901).scalar()
    sum_delivery_price = db.session.query(func.sum(ProductOrder.price * ProductOrder.qty)).filter(func.date(ProductOrder.date) == target)\
        .filter(ProductOrder.item == 901).scalar()
    total_price = db.session.query(func.sum(ProductOrder.price * ProductOrder.qty)).filter(func.date(ProductOrder.date) == target)\
        .scalar()

    return render_template('order/data.html', target=target, orders=orders, sum_qty=sum_qty, sum_price=sum_price,
    sum_delivery_price=sum_delivery_price, total_price=total_price)


@order.route('/range')
@login_required
def date_range():

    page = request.args.get('page', 1, type=int)
    date_from = request.args.get('date_from')
    date_to = request.args.get('date_to')

    if date_from and date_to:
        orders = ProductOrder.query.filter(func.DATE(ProductOrder.date) <= date_to).filter(func.DATE(ProductOrder.date) >= date_from)\
            .paginate(page=page, per_page=100)

        return render_template('order/range.html', date_from=date_from, date_to=date_to, orders=orders)

    return render_template('order/range.html')
