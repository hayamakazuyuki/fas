from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user, login_required

from .extentions import db
from .models import CustomerUser, Shop, ProductOrder
from .forms import CustomerOrderForm

cs = Blueprint('cs', __name__)


@cs.route('/')
@login_required
def index():
    customer_id = current_user.customer_id
    shop_id = current_user.shop_id

    form = CustomerOrderForm()

    shop = Shop.query.get_or_404((customer_id, shop_id))
    orders = ProductOrder.query.filter_by(customer_id=customer_id).filter_by(shop_id=shop_id).order_by(ProductOrder.id.desc()).all()

    return render_template('index.html', shop=shop, orders=orders, form=form)


@cs.route('/order', methods=['POST'])
@login_required
def order():

    customer_id = current_user.customer_id
    shop_id = current_user.shop_id

    order = ProductOrder()
    order.sales_by = 10
    order.customer_id = customer_id
    order.shop_id = shop_id
    order.item = request.form['item']

    if request.form['item'] == '602':
        price = 3400
    elif request.form['item'] == '603':
        price = 3300
    else:
        price = 3000

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
