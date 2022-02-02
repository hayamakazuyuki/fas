from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required

from ..models import Product
from .forms import CustomerForm
from app import db

main = Blueprint('main', __name__)


@main.route('/')
@login_required
def index():
    return render_template('index.html')

@main.route('/test')
@login_required
def test():
    return 'テスト'



# @main.route('/customer')
# def customer():

#     if not request.args:
#         return render_template('customer/customer.html')

    # else:
    #     search_string = request.args.get('search_string')

    #     if search_string.isdigit():
    #         customer_id = search_string
    #         result = Customer.query.get(customer_id)

    #         if result:
    #             return redirect(url_for('main.customer_profile', id=customer_id))
    #         else:
    #             return render_template('customer/customer.html')

    #     else:
    #         search_value = "%{}%".format(search_string)
    #         page = request.args.get('page', default=1, type=int)
    #         result = Customer.query.filter(Customer.name.like(search_value)).paginate(page=page, per_page=20)
    #         result_length = len(Customer.query.filter(Customer.name.like(search_value)).all())
    #         return render_template('customer/customer.html', customers=result, result_length=result_length,
    #                                search_string=search_string)


# register customers
@main.route('/customer/register', methods=['GET', 'POST'])
def customer_register():
    form = CustomerForm()

    if form.validate_on_submit():
        id = request.form['id']
        name = request.form['name']

        # check if requested id already exists in the db
        exists = Customer.query.get(id)
        
        if exists:
            return redirect(url_for('main.customer_profile', id=id))
        else:
            new_customer = Customer(id=id, name=name)
            db.session.add(new_customer)
            db.session.commit()

            flash('新規取引先を登録しました。', 'success')
            return redirect(url_for('main.customer_profile', id=id))

    return render_template('customer/customer_register.html', form=form)


# show and update customer profile
@main.route('/customer/<int:id>', methods=['GET', 'POST'])
def customer_profile(id):
    page = request.args.get('page', 1, type=int)
    mode = request.args.get('mode')
    customer = Customer.query.get_or_404(id)

    all_shops = Shop.query.filter_by(customer_id=id).paginate(page=page, per_page=20)
    form = CustomerForm()

    if mode == 'edit':
        if request.method == 'POST':
            customer.name = request.form['name']
            db.session.commit()
            return redirect(url_for('main.customer_profile', id=id))

        return render_template('customer_update.html', customer=customer, form=form)

    else:

        return render_template('customer/customer_profile.html', customer=customer, shops=all_shops)


# show products/items list
@main.route('/product')
def product():

    products = Product.query.all()
    return render_template('products.html', products=products)

