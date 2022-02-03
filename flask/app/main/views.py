from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required

from ..models import Product

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


# show products/items list
@main.route('/product')
def product():

    products = Product.query.all()
    return render_template('products.html', products=products)

