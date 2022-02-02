from flask import Blueprint, request, render_template, make_response
from datetime import datetime, timedelta, timezone
from flask_login import login_required

from io import StringIO

import csv

from sqlalchemy import func

order_data = Blueprint('order_data', __name__, url_prefix='/order_data')
JST = timezone(timedelta(hours=+9), 'JST')


@order_data.route('/', methods=['GET', 'POST'])
@login_required
def index():

    return render_template('order_data/index.html')


@order_data.route('/range')
@login_required
def date_range():
    page = request.args.get('page', 1, type=int)

    date_from = request.args.get('date_from')
    date_to = request.args.get('date_to')

    if date_from and date_to:
    
        return render_template('order_data/range.html', date_from=date_from, date_to=date_to)

    else:
        return render_template('order_data/range.html', date_from=date_from, date_to=date_to)
