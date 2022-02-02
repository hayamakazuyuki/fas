from flask import Blueprint, request, render_template

customer = Blueprint('customer', __name__, url_prefix='/customer')

@customer.route('/')
def index():
    
    if not request.args:
        return render_template('customer/customer.html')

