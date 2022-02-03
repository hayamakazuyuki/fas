from crypt import methods
from flask import Blueprint, render_template, request
from flask_login import login_required

from ..models import Shop


order = Blueprint('order', __name__, url_prefix='/order')

@order.route('/', methods=['GET', 'POST'])
@login_required
def index():

    customer_id = request.args.get('customer_id')
    id = request.args.get('id')
    
    shop = Shop.query.get((customer_id, id))

    return render_template('order/register.html', shop=shop)
