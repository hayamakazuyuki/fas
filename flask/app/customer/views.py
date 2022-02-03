from flask import Blueprint, request, render_template, redirect, url_for, flash
from ..extentions import db
from ..models import Customer, Shop
from .forms import CustomerForm


customer = Blueprint('customer', __name__, url_prefix='/customer')

@customer.route('/')
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
            return redirect(url_for('customer.profile', id=id))

        return render_template('customer/update.html', customer=customer, form=form)

    else:
        return render_template('customer/profile.html', customer=customer, shops=shops)
