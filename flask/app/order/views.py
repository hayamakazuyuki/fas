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
        new_order = ProductOrder()
        new_order.sales_by = staff
        new_order.customer_id = customer_id
        new_order.shop_id = id
        new_order.item = request.form['item']
        new_order.price = request.form['price']
        new_order.qty = request.form['qty']
        new_order.delivery_check = request.form.get('noDelivery')

        db.session.add(new_order)


        # if delivery:
        #     sales_by = staff
        #     customer_id = customer_id
        #     id = id
        #     item = request.form['delivery']
        #     price = request.form['deliveryPrice']
        #     qty = request.form['deliveryQty']
        
        db.session.commit()

        return redirect(url_for('customer.index'))

        # if item2:
        #     sales_by = staff
        #     customer_id = customer_id
        #     id = id
        #     item = request.form['item2']
        #     price = request.form['price2']
        #     qty = request.form['qty2']
        #     delivery_check = request.form.get('noDelivery2')
            
        #     return f'{item}'

    return render_template('order/register.html', shop=shop)
