from flask import Blueprint, render_template, request
from flask_login import login_required
from ..calcs import get_total_qty, get_total_amount, get_sum_by_item, get_sum_by_staff
import datetime

downloads = Blueprint('downloads', __name__, url_prefix='/downloads')
JST = datetime.timezone(datetime.timedelta(hours=+9), 'JST')


@downloads.route('/')
@login_required
def index():

    target_date = request.args.get('targetDate')
    from_date = request.args.get('fromDate')
    to_date = request.args.get('toDate')

    if from_date and to_date:

        total_qty = get_total_qty(target_date, from_date, to_date)
        total_amount = get_total_amount(target_date, from_date, to_date)
        sum_by_item = get_sum_by_item(target_date, from_date, to_date)
        sum_by_staff = get_sum_by_staff(target_date, from_date, to_date)

    else:

        if not target_date:
            target_date = datetime.datetime.now(JST).strftime('%Y-%m-%d')

        else:
            pass

        total_qty = get_total_qty(target_date, from_date, to_date)
        total_amount = get_total_amount(target_date, from_date, to_date)
        sum_by_item = get_sum_by_item(target_date)
        sum_by_staff = get_sum_by_staff(target_date, from_date, to_date)

    return render_template('downloads/index.html', target_date=target_date, from_date=from_date, to_date=to_date,
     total_qty=total_qty, total_amount=total_amount, sum_by_item=sum_by_item, sum_by_staff=sum_by_staff)
