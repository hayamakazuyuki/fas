from flask import Blueprint, render_template
import datetime
import requests
import os
from .calcs import get_total_qty, get_total_amount, get_sum_by_item, get_sum_by_staff

scheduled = Blueprint('scheduled', __name__)

JST = datetime.timezone(datetime.timedelta(hours=+9), 'JST')
now = datetime.datetime.now(JST)

# cron.yaml every day 00:05
@scheduled.route('/daily-report')
def daily_report():

    yesterday = now - datetime.timedelta(days=1)

    # summary
    total_qty = get_total_qty(yesterday)
    total_amount = get_total_amount(yesterday)

    # group by item and staff
    # sum_by_item = get_sum_by_item(yesterday)
    sum_by_staff = get_sum_by_staff(yesterday)

    body = render_template('daily-report.txt', now=now, yesterday=yesterday, total_qty=total_qty, total_amount=total_amount, 
            sum_by_staff=sum_by_staff)

    api_key = os.environ.get('X_CHATWORK_TOKEN')
    url = "https://api.chatwork.com/v2/rooms/281437593/messages"

    headers = {
        "x-chatworktoken": api_key
        }

    params = { "self_unread" : 1,
                "body" : body }

    response = requests.post(url, headers=headers, params=params)

    return ('', 204)
