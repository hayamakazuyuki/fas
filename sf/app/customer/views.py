from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import login_required
from ..extentions import db
from ..models import Customer, Shop, ProductOrder, Product, CustomerContractPrice
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
        register_items = request.form.get('registerItems')

        # check if requested id already exists in the db
        exists = Customer.query.get(id)
        
        if exists:
            return redirect(url_for('customer.profile', id=id))
        else:
            new_customer = Customer(id=id, name=name, staff=staff)
            db.session.add(new_customer)
            db.session.commit()

            if register_items:

                flash('新規取引先を登録しました。', 'success')

                return redirect(url_for('customer.register_contract_price', id=id))

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

    items_prices = CustomerContractPrice.query.filter_by(customer_id=id).all() 
    registered_items = len(CustomerContractPrice.query.filter_by(customer_id=id).all())

    if mode == 'edit':

        form = CustomerRegisterForm(obj=customer)

        if form.validate_on_submit():
            customer.name = request.form['name']
            customer.staff = request.form['staff']
            db.session.commit()
            
            flash('取引先情報を更新しました。', 'success')

            return redirect(url_for('customer.profile', id=id))

        return render_template('customer/update.html', customer=customer, form=form)

    return render_template('customer/profile.html', customer=customer, shops=shops, items_prices=items_prices, registered_items=registered_items)


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


@customer.route('/<int:id>/register-contract-price', methods=['GET', 'POST'])
@login_required
def register_contract_price(id):

    customer = Customer.query.get(id)
    items = Product.query.all()

    if request.method == 'POST':
        item1 = request.form['item1']
        item2 = request.form.get('item2')
        item3 = request.form.get('item3')
        item4 = request.form.get('item4')
        item5 = request.form.get('item5')


        item_price = CustomerContractPrice(customer_id=id, product_id=item1, price=request.form['itemPrice1'])
        db.session.add(item_price)

        if item2:
            item_price = CustomerContractPrice(customer_id=id, product_id=item2, price=request.form['itemPrice2'])
            db.session.add(item_price)

        if item3:
            item_price = CustomerContractPrice(customer_id=id, product_id=item3, price=request.form['itemPrice3'])
            db.session.add(item_price)

        if item4:
            item_price = CustomerContractPrice(customer_id=id, product_id=item4, price=request.form['itemPrice4'])
            db.session.add(item_price)

        if item5:
            item_price = CustomerContractPrice(customer_id=id, product_id=item5, price=request.form['itemPrice5'])
            db.session.add(item_price)

        db.session.commit()

        flash('商品と単価を登録しました。', 'success')

        return redirect(url_for('customer.profile', id=id))

    return render_template('customer/register-contract-price.html', customer=customer, items=items)


@customer.route('/<int:id>/add-contract-price', methods=['GET', 'POST'])
@login_required
def add_contract_price(id):

    customer = Customer.query.get(id)
    registered_items = CustomerContractPrice.query.filter_by(customer_id=id).all()

    filter_list = []
    for registered_item in registered_items:
        filter_list.append(registered_item.product_id)

    items = Product.query.filter(Product.id.not_in(filter_list)).all()
    

    if request.method == 'POST':
        item2 = request.form.get('item2')
        item3 = request.form.get('item3')
        item4 = request.form.get('item4')
        item5 = request.form.get('item5')

        if item2:
            item_price = CustomerContractPrice(customer_id=id, product_id=item2, price=request.form['itemPrice2'])
            db.session.add(item_price)

        if item3:
            item_price = CustomerContractPrice(customer_id=id, product_id=item3, price=request.form['itemPrice3'])
            db.session.add(item_price)

        if item4:
            item_price = CustomerContractPrice(customer_id=id, product_id=item4, price=request.form['itemPrice4'])
            db.session.add(item_price)

        if item5:
            item_price = CustomerContractPrice(customer_id=id, product_id=item5, price=request.form['itemPrice5'])
            db.session.add(item_price)

        db.session.commit()

        flash('商品と単価を追加しました。', 'success')

        return redirect(url_for('customer.profile', id=id))

    return render_template('customer/add-contract-price.html', customer=customer, registered_items=registered_items, items=items)


@customer.route('/<int:customer_id>/edit-contract-price/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_contract_price(customer_id, id):

    customer = Customer.query.get(customer_id)
    items = Product.query.all()

    registered_item = CustomerContractPrice.query.get(id)

    if request.method == 'POST':
        new_price = int(request.form['price'])

        if new_price == registered_item.price:
            
            flash('単価の変更はありません。', 'info')
            return redirect(url_for('customer.profile', id=customer.id))

        else:
            registered_item.price = new_price
            db.session.commit()

            flash('単価を変更しました。', 'success')

            return redirect(url_for('customer.profile', id=customer.id))

    return render_template('customer/edit-contract-price.html', customer=customer, items=items, registered_item=registered_item)


@customer.route('/<int:customer_id>/delete-contract-price/<int:id>')
@login_required
def delete_contract_price(customer_id, id):

    registered_item = CustomerContractPrice.query.get(id)
    db.session.delete(registered_item)
    db.session.commit()
    
    flash('登録商品と単価を削除しました。', 'success')

    return redirect(url_for('customer.profile', id=customer_id))
