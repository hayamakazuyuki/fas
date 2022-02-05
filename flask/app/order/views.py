from crypt import methods
from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import current_user, login_required

from ..extentions import db

from ..models import Shop, ProductOrder


order = Blueprint('order', __name__, url_prefix='/order')

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
    return 'データ'
    