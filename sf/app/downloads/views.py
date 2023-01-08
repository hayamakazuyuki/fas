from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required
from ..calcs import get_total_qty, get_total_amount, get_sum_by_item, get_sum_by_staff, get_orders
import datetime

downloads = Blueprint('downloads', __name__, url_prefix='/downloads')
JST = datetime.timezone(datetime.timedelta(hours=+9), 'JST')


@downloads.route('/')
@login_required
def index():

    target_date = datetime.datetime.now(JST).strftime('%Y-%m-%d')

    total_qty = get_total_qty(target_date)
    total_amount = get_total_amount(target_date)
    sum_by_item = get_sum_by_item(target_date)
    sum_by_staff = get_sum_by_staff(target_date)

    return render_template('downloads/index.html', target_date=target_date, total_qty=total_qty,
         total_amount=total_amount, sum_by_item=sum_by_item, sum_by_staff=sum_by_staff)




@downloads.route('/<type>')
@login_required
def download_csv(type):

    if type == 'today':
        
        target_date = datetime.datetime.now(JST).strftime('%Y-%m-%d')
        orders = get_orders(target_date)

        return '今日'

    elif type == 'search':

        target_date = request.args.get('targetDate')
        from_date = request.args.get('fromDate')
        to_date = request.args.get('toDate')

        total_qty = get_total_qty(target_date, from_date, to_date)
        total_amount = get_total_amount(target_date, from_date, to_date)
        sum_by_item = get_sum_by_item(target_date, from_date, to_date)
        sum_by_staff = get_sum_by_staff(target_date, from_date, to_date)

        return render_template('downloads/searched.html', target_date=target_date, from_date=from_date, to_date=to_date,
         total_qty=total_qty, total_amount=total_amount, sum_by_item=sum_by_item, sum_by_staff=sum_by_staff)

    else:
        return redirect(url_for('.index'))
