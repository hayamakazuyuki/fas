from flask import Blueprint, request, render_template, redirect, url_for
from ..models import Customer


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


