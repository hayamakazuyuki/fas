from email.policy import default
from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import login_required
from ..extentions import db
from ..models import Customer, Shop, ProductOrder
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
            return redirect(url_for('customer.profile', id=q))
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


@customer.route('/shop/')
@login_required
def shop():

    q = request.args.get('q')

    if not q:
        return render_template('customer/customer.html')

    search = "%{}%".format(q)
    page = request.args.get('page', default=1, type=int)
    shops = Shop.query.filter(Shop.name.like(search)).paginate(page=page, per_page=20)
    count = len(Shop.query.filter(Shop.name.like(search)).all())

    return render_template('customer/customer.html', shops=shops, count=count, q=q)


# register shop
@customer.route('/shop/register', methods=['GET', 'POST'])
@login_required
def shop_register():

    form = ShopForm()
    customer_id = request.args.get('customer_id')

    if form.validate_on_submit():
        customer_id = request.form['customer_id']
        id = request.form['id']

        # check if shop already exists in the db
        exists = Shop.query.get((customer_id, id))

        if exists:
            return redirect(url_for('customer.shop_profile', customer_id=customer_id, id=id))

        new_shop = Shop()
        new_shop.customer_id = request.form['customer_id']
        new_shop.id = request.form['id']
        new_shop.name = request.form['name']
        new_shop.department = request.form['department']
        new_shop.zip = request.form['zip']
        new_shop.prefecture = request.form['prefecture']
        new_shop.city = request.form['city']
        new_shop.town = request.form['town']
        new_shop.address = request.form['address']
        new_shop.building = request.form['building']
        new_shop.email = request.form['email']
        new_shop.telephone = request.form['telephone']

        db.session.add(new_shop)
        db.session.commit()

        flash('事業所を登録しました。', 'success')

        return redirect(url_for('customer.profile', id=customer_id))
    
    return render_template('customer/shop-register.html', form=form, customer_id=customer_id)


# show shop information
@customer.route('/shop/<int:customer_id>/<int:id>', methods=['GET', 'POST'])
@login_required
def shop_profile(customer_id, id):

    shop = Shop.query.get_or_404((customer_id, id))
    orders = ProductOrder.query.filter_by(customer_id=customer_id).filter_by(shop_id=id).order_by(ProductOrder.id.desc()).all()
    
    mode = request.args.get('mode')

    if mode == 'edit':
        form = ShopForm()

        if request.method == 'POST':
            shop.name = request.form['name']
            shop.department = request.form['department']
            shop.zip = request.form['zip']
            shop.prefecture = request.form['prefecture']
            shop.city = request.form['city']
            shop.town = request.form['town']
            shop.address = request.form['address']
            shop.building = request.form['building']
            shop.email = request.form['email']
            shop.telephone = request.form['telephone']

            db.session.commit()

            flash('事業所の情報を更新しました。', 'success')

            return redirect(url_for('customer.shop_profile', customer_id=customer_id, id=id))

        return render_template('customer/shop-update.html', shop=shop, form=form)

    return render_template('customer/shop-profile.html', shop=shop, orders=orders)

