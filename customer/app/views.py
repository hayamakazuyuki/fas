from datetime import datetime
from itertools import product
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user, login_required
from sqlalchemy import func

from .extentions import db
from .models import JST, Customer, Shop, ProductOrder, CustomerPrice


cs = Blueprint('cs', __name__)


@cs.route('/')
@login_required
def index():
    customer_id = current_user.customer_id
    shop_id = current_user.shop_id

    shop = Shop.query.get_or_404((customer_id, shop_id))
    orders = ProductOrder.query.filter_by(customer_id=customer_id).filter_by(shop_id=shop_id).order_by(ProductOrder.id.desc()).all()

    items = CustomerPrice.query.filter_by(customer_id=customer_id).all()

    return render_template('index.html', shop=shop, orders=orders, items=items)


@cs.route('/order', methods=['POST'])
@login_required
def order():

    customer_id = current_user.customer_id
    shop_id = current_user.shop_id
    customer = Customer.query.get(customer_id)

    order = ProductOrder()
    order.sales_by = customer.staff
    order.customer_id = customer_id
    order.shop_id = shop_id
    product = request.form['item']

    order.item = product

    # get the contract price for the item of the customer
    item_price = CustomerPrice.query.filter(CustomerPrice.customer_id == customer_id, CustomerPrice.product_id == product).first()
    price = item_price.price

    order.price = price
    order.qty = request.form['qty']

    db.session.add(order)
    db.session.commit()
        
    flash('商品を発注しました。', 'success')

    return redirect(url_for('cs.index'))


# delete order
@cs.route('/delete/<int:id>')
@login_required
def order_delete(id):
    order = ProductOrder.query.get(id)
    db.session.delete(order)
    db.session.commit()

    flash('注文を削除しました。', 'warning')

    return redirect(url_for('cs.index'))


@cs.route('/stats')
@login_required
def stats():
    target = request.args.get("target")
    customer_id = current_user.customer_id

    if target is None:
        today = datetime.now(JST)
        target = today.strftime('%Y-%m-%d')

    orders = ProductOrder.query.filter(ProductOrder.customer_id == customer_id).filter(func.DATE(ProductOrder.date) == target).all()

    return render_template('stats.html', target=target, orders=orders)
