from datetime import datetime, timezone, timedelta
from flask import Blueprint, render_template, request, redirect, url_for, make_response, flash
from flask_login import current_user, login_required
from sqlalchemy import func
from io import StringIO
import csv

from ..extentions import db

from ..models import DeliveryRequest, Shop, ProductOrder, Customer, Shipping

from .forms import order_edit_form, DeliveryRequestForm


order = Blueprint('order', __name__, url_prefix='/order')

JST = timezone(timedelta(hours=+9), 'JST')

@order.route('/<int:customer_id>/<int:id>')
@login_required
def index(customer_id, id):

    customer = Customer.query.get(customer_id)

    if not customer.staff:
        return redirect(url_for('customer.profile', id=customer_id, mode='edit'))

    else:
        return redirect(url_for('order.register', customer_id=customer_id, id=id))


@order.route('/<int:customer_id>/<int:id>/register', methods=['GET', 'POST'])
@login_required
def register(customer_id, id):

    shop = Shop.query.get((customer_id, id))

    # generate min and max dates for delivery date request.
    min_date = datetime.now(JST) + timedelta(days=4)
    max_date = datetime.now(JST) + timedelta(days=29)

    if request.method == 'POST':

        staff = shop.customer.staff

        item2 = request.form.get('item2')
        item3 = request.form.get('item3')

        delivery_date = request.form.get('delivery_date')
        time_range = request.form.get('time_range')
        memo = request.form.get('memo')
        delivery = request.form.get('delivery')

        # item
        order = ProductOrder()
        order.sales_by = staff
        order.customer_id = customer_id
        order.shop_id = id
        order.item = request.form['item']
        order.price = request.form['price']
        order.qty = request.form['qty']
        # order.delivery_check = request.form.get('noDelivery')

        db.session.add(order)
        db.session.commit()

        if delivery_date or time_range or memo:
            order_id = order.id
            delivery_request = DeliveryRequest()

            delivery_request.order_id = order_id
            delivery_request.requested_by = current_user.id
            if delivery_date:
                delivery_request.delivery_date = delivery_date
            delivery_request.time_range = time_range
            delivery_request.memo = memo

            db.session.add(delivery_request)
            db.session.commit()

        if item2:
            order2 = ProductOrder()
            order2.sales_by = staff
            order2.customer_id = customer_id
            order2.shop_id = id
            order2.item = request.form['item2']
            order2.price = request.form['price2']
            order2.qty = request.form['qty2']
            # order2.delivery_check = request.form.get('noDelivery2')

            db.session.add(order2)
            db.session.commit()

            if delivery_date or time_range or memo:
                order_id = order2.id
                delivery_request = DeliveryRequest()

                delivery_request.order_id = order_id
                delivery_request.requested_by = current_user.id
                if delivery_date:
                    delivery_request.delivery_date = delivery_date
                delivery_request.time_range = time_range
                delivery_request.memo = memo

                db.session.add(delivery_request)
                db.session.commit()

        if item3:
            order3 = ProductOrder()
            order3.sales_by = staff
            order3.customer_id = customer_id
            order3.shop_id = id
            order3.item = request.form['item3']
            order3.price = request.form['price3']
            order3.qty = request.form['qty3']
            # order3.delivery_check = request.form.get('noDelivery3')

            db.session.add(order3)
            db.session.commit()

            if delivery_date or time_range or memo:
                order_id = order3.id

                delivery_request = DeliveryRequest()

                delivery_request.order_id = order_id
                delivery_request.requested_by = current_user.id
                if delivery_date:
                    delivery_request.delivery_date = delivery_date
                delivery_request.time_range = time_range
                delivery_request.memo = memo

                db.session.add(delivery_request)
                db.session.commit()

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

        flash('受注を登録しました。', 'success')

        return redirect(url_for('main.index'))

    return render_template('order/register.html', shop=shop, min_date=min_date, max_date=max_date)


@order.route('/<int:id>')
@order.route('/<int:id>/<edit>', methods=['GET', 'POST'])
@login_required
def order_detail(id, edit=None, request_id=None):

    order = ProductOrder.query.get(id)
    # mode = request.args.get('mode')

    # get 2hours before and remove timezone info
    # before2hours = datetime.now(JST) - timedelta(seconds=7200)
    # before2h = before2hours.replace(tzinfo=None)

 
    if edit == 'order':
        current_item = order.product.id
        OrderEditForm = order_edit_form(current_item)

        form = OrderEditForm()

        if form.validate_on_submit():
            order.item = request.form['item']
            order.price = request.form['price']
            order.qty = request.form['qty']
            db.session.commit()

            flash('受注内容を変更しました。', 'success')
            return redirect(url_for('order.order_detail', id=id))

        return render_template('order/order-edit.html', order=order, form=form)

    return render_template('order/order-detail.html', order=order)


@order.route('/<int:id>/request/', methods=['GET', 'POST'])
@order.route('/<int:id>/request/<int:request_id>', methods=['GET', 'POST'])
@login_required
def order_request(id, request_id=None):

    order = ProductOrder.query.get(id)

    # generate min and max dates for delivery date request.
    min_date = datetime.now(JST) + timedelta(days=4)
    max_date = datetime.now(JST) + timedelta(days=29)

    if request_id:

        delivery_request = DeliveryRequest.query.get(request_id)
        form = DeliveryRequestForm(obj=delivery_request)

        if form.validate_on_submit():
            delivery_date = request.form.get('delivery_date')

            if delivery_date:
                delivery_request.delivery_date = delivery_date
            else:
                delivery_request.delivery_date = None
            delivery_request.time_range = request.form.get('time_range')
            delivery_request.memo = request.form.get('memo')

            if order.delivery_check is None:
                db.session.commit()
                flash('配送依頼を変更しました。', 'success')

            else:
                flash('配送依頼は既にダウンロードされています.', 'error')
            
            return redirect(url_for('order.order_detail', id=id))

    elif not request_id:

        form = DeliveryRequestForm()

        if form.validate_on_submit():
            delivery_request = DeliveryRequest()
            delivery_request.order_id = id
            delivery_request.requested_by = current_user.id
            if request.form.get('delivery_date'):
                delivery_request.delivery_date = request.form.get('delivery_date')
            delivery_request.time_range = request.form.get('time_range')
            delivery_request.memo = request.form.get('memo')

            if order.delivery_check is None:

                db.session.add(delivery_request)
                db.session.commit()
    
                flash('配送依頼を登録しました。', 'success')

            else:
                flash('配送依頼は既にダウンロードされています.', 'error')

            return redirect(url_for('order.order_detail', id=id))

    return render_template('order/order-request-edit.html', order=order, form=form, min_date=min_date, max_date=max_date)


# delete order
@order.route('/delete/<int:id>')
@login_required
def order_delete(id):
    order = ProductOrder.query.get(id)
    db.session.delete(order)
    db.session.commit()

    flash('注文を削除しました。', 'warning')

    return redirect(url_for('main.index'))


@order.route('/data')
@login_required
def data():
    target = request.args.get("target")
    dl = request.args.get('dl')

    if target is None:
        today = datetime.now(JST)
        target = today.strftime('%Y-%m-%d')

    orders = ProductOrder.query.filter(func.DATE(ProductOrder.date) == target).all()
    shippings = Shipping.query.all() # for testing

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
    sum_delivery_price=sum_delivery_price, total_price=total_price, shippings=shippings)


@order.route('/range')
@login_required
def range():

    page = request.args.get('page', 1, type=int)
    date_from = request.args.get('date_from')
    date_to = request.args.get('date_to')

    range_orders = ProductOrder.query.filter(func.DATE(ProductOrder.date) <= date_to).filter(func.DATE(ProductOrder.date) >= date_from)\
        .paginate(page=page, per_page=100)

    r_sum_qty = db.session.query(func.sum(ProductOrder.qty)).filter(ProductOrder.item != 901)\
        .filter(func.date(ProductOrder.date) >= date_from).filter(func.date(ProductOrder.date) <= date_to)\
        .scalar()
    r_sum_price = db.session.query(func.sum(ProductOrder.price * ProductOrder.qty)).filter(ProductOrder.item != 901)\
        .filter(func.date(ProductOrder.date) >= date_from).filter(func.date(ProductOrder.date) <= date_to).scalar()
    r_sum_delivery_price = db.session.query(func.sum(ProductOrder.price * ProductOrder.qty)).filter(ProductOrder.item == 901)\
        .filter(func.date(ProductOrder.date) >= date_from).filter(func.date(ProductOrder.date) <= date_to).scalar()
    r_total_price = db.session.query(func.sum(ProductOrder.price * ProductOrder.qty))\
        .filter(func.date(ProductOrder.date) >= date_from).filter(func.date(ProductOrder.date) <= date_to)\
        .scalar()

    return render_template('order/data.html', date_from=date_from, date_to=date_to, range_orders=range_orders,
    r_sum_qty=r_sum_qty, r_sum_price=r_sum_price, r_sum_delivery_price=r_sum_delivery_price, r_total_price=r_total_price)


@order.route('/invoice_data')
@order.route('/invoice_data/<dl>')
@login_required
def invoice_data(dl=None):

    orders = ProductOrder.query.filter(ProductOrder.exported.is_(None)).all()
    orders_count = len(orders)

    if dl == 'csv':

        today = datetime.now(JST)
        file_date = today.strftime('%Y-%m-%d')

        file = StringIO()
        writer = csv.writer(file, lineterminator="\n")

        writer.writerow(['顧客ID', '事業所ID', '受注日', '商品番号', 'KBN', '単価', '数量', '手数料', '商品名'])
        for order in orders:
            writer.writerow(
                [order.customer_id, order.shop_id, order.date, order.item, 1, order.price, order.qty, 0,
                 order.product.name])
    
        response = make_response()
        response.data = file.getvalue().encode('sjis', 'replace')
        response.headers['Content-Type'] = 'text/csv'
        response.headers['Content-Disposition'] = 'attachment; filename=brycenData-' + file_date + '.csv'

        for order in orders:
            order.exported = 1
        db.session.commit()

        return response

    return render_template('order/invoice_data.html', orders_count=orders_count)