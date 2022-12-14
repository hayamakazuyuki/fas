from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import login_required
from ..extentions import db
from ..models import Customer, Shop, ProductOrder
from .forms import ShopForm, CustomerRegisterForm


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

    form = CustomerRegisterForm()

    if form.validate_on_submit():
        id = request.form['id']
        name = request.form['name']
        staff = request.form['staff']

        # check if requested id already exists in the db
        exists = Customer.query.get(id)
        
        if exists:
            return redirect(url_for('customer.profile', id=id))
        else:
            new_customer = Customer(id=id, name=name, staff=staff)
            db.session.add(new_customer)
            db.session.commit()

            flash('新規取引先を登録しました。', 'success')
            return redirect(url_for('customer.profile', id=id))

    return render_template('customer/register.html', form=form)


# show and update customer profile
@customer.route('/<int:id>')
@customer.route('/<int:id>/<mode>', methods=['GET', 'POST'])
@login_required
def profile(id, mode=None):

    page = request.args.get('page', 1, type=int)
    customer = Customer.query.get_or_404(id)

    shops = Shop.query.filter_by(customer_id=id).paginate(page=page, per_page=20)

    if mode == 'edit':

        form = CustomerRegisterForm(obj=customer)

        if form.validate_on_submit():
            customer.name = request.form['name']
            customer.staff = request.form['staff']
            db.session.commit()
            
            flash('取引先情報を更新しました。', 'success')

            return redirect(url_for('customer.profile', id=id))

        return render_template('customer/update.html', customer=customer, form=form)

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
@customer.route('/<int:customer_id>/register', methods=['GET', 'POST'])
@login_required
def shop_register(customer_id):

    form = ShopForm()
    customer = Customer.query.get(customer_id)

    if form.validate_on_submit():

        id = request.form['id']

        # check if the shop already exists in the db
        exists = Shop.query.get((customer_id, id))

        if exists:
            return redirect(url_for('customer.shop_profile', customer_id=customer_id, id=id))

        new_shop = Shop()
        new_shop.customer_id = customer_id
        new_shop.id = request.form['id']
        new_shop.shop_number = request.form.get('shop_number')
        new_shop.name = request.form['name']
        new_shop.department = request.form.get('department')
        new_shop.zip = request.form['zip']
        new_shop.prefecture = request.form['prefecture']
        new_shop.city = request.form['city']
        new_shop.town = request.form['town']
        new_shop.address = request.form['address']
        new_shop.building = request.form.get('building')
        new_shop.telephone = request.form['telephone']

        db.session.add(new_shop)
        db.session.commit()

        flash('事業所を登録しました。', 'success')

        return redirect(url_for('customer.profile', id=customer_id))
    
    return render_template('customer/shop-register.html', form=form, customer=customer)


# show and update shop information
@customer.route('<int:customer_id>/<int:id>')
@customer.route('<int:customer_id>/<int:id>/<mode>', methods=['GET', 'POST'])
@login_required
def shop_profile(customer_id, id, mode=None):

    shop = Shop.query.get_or_404((customer_id, id))
    orders = ProductOrder.query.filter_by(customer_id=customer_id).filter_by(shop_id=id).order_by(ProductOrder.id.desc()).all()

    if mode == 'edit':
        form = ShopForm(obj=shop)

        if request.method == 'POST':
            shop.name = request.form['name']
            shop.shop_number = request.form.get('shop_number')
            shop.department = request.form.get('department')
            shop.zip = request.form['zip']
            shop.prefecture = request.form['prefecture']
            shop.city = request.form['city']
            shop.town = request.form['town']
            shop.address = request.form.get('address')
            shop.building = request.form.get('building')
            shop.telephone = request.form['telephone']

            db.session.commit()

            flash('事業所の情報を更新しました。', 'success')

            return redirect(url_for('customer.shop_profile', customer_id=customer_id, id=id))

        return render_template('customer/shop-update.html', shop=shop, form=form)

    return render_template('customer/shop-profile.html', shop=shop, orders=orders)


@customer.route('/<int:id>/register-contract-price')
@login_required
def register_contract_price(id):

    customer = Customer.query.get(id)
    # form = ContractPriceForm()

    return render_template('customer/register-contract-price.html', customer=customer)
