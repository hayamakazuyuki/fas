from email.policy import default
from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import login_required
from ..extentions import db
from ..models import Customer, Shop
from .forms import CustomerForm, ShopForm


customer = Blueprint('customer', __name__, url_prefix='/customer')

@customer.route('/')
@login_required
def index():
    
    if not request.args:
        return render_template('customer/customer.html')

    q = request.args.get('q')

    if q.isdigit():
        q = q
        result = Customer.query.get(q)

        if result:
            return 'ある'
        else:
            return redirect(url_for('customer.index'))

    search = "%{}%".format(q)

    page = request.args.get('page', default=1, type=int)
    result = Customer.query.filter(Customer.name.like(search)).paginate(page=page, per_page=20)
    count = len(Customer.query.filter(Customer.name.like(search)).all())
    return render_template('customer/customer.html', customers=result, count=count, search=search)


# register customer
@customer.route('/register', methods=['GET', 'POST'])
@login_required
def register():
    form = CustomerForm()

    if form.validate_on_submit():
        id = request.form['id']
        name = request.form['name']

        # check if requested id already exists in the db
        exists = Customer.query.get(id)
        
        if exists:
            return redirect(url_for('customer.profile', id=id))
        else:
            new_customer = Customer(id=id, name=name)
            db.session.add(new_customer)
            db.session.commit()

            flash('新規取引先を登録しました。', 'success')
            return redirect(url_for('customer.profile', id=id))

    return render_template('customer/register.html', form=form)


# show and update customer profile
@customer.route('/<int:id>', methods=['GET', 'POST'])
@login_required
def profile(id):
    page = request.args.get('page', 1, type=int)
    mode = request.args.get('mode')
    customer = Customer.query.get_or_404(id)
    
    shops = Shop.query.filter_by(customer_id=id).paginate(page=page, per_page=20)

    form = CustomerForm()

    if mode == 'edit':
        if request.method == 'POST':
            customer.name = request.form['name']
            db.session.commit()
            
            flash('取引先情報を更新しました。', 'success')

            return redirect(url_for('customer.profile', id=id))

        return render_template('customer/update.html', customer=customer, form=form)

    else:
        return render_template('customer/profile.html', customer=customer, shops=shops)


@customer.route('/shop')
@login_required
def shop():

    q = request.args.get('q')

    if not q:
        return render_template('customer/shop.html')

    search = "%{}%".format(q)
    page = request.args.get('page', default=1, type=int)
    shops = Shop.query.filter(Shop.name.like(search)).paginate(page=page, per_page=20)
    count = len(Shop.query.filter(Shop.name.like(search)).all())

    return render_template('customer/shop.html', shops=shops, count=count, q=q)


@customer.route('/shop/register', methods=['GET', 'POST'])
@login_required
def shop_register():

    form = ShopForm()
    customer_id = request.args.get('customer_id')


    return render_template('customer/shop-register.html', form=form, customer_id=customer_id)
