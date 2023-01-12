from flask import Blueprint, render_template
import datetime
import requests
import os
from .calcs import get_total_qty, get_total_amount

scheduled = Blueprint('scheduled', __name__)

JST = datetime.timezone(datetime.timedelta(hours=+9), 'JST')
now = datetime.datetime.now(JST)


@scheduled.route('/daily-report')
def daily_report():

    yesterday = now - datetime.timedelta(days=1)

    api_key = os.environ.get('X_CHATWORK_TOKEN')
    url = "https://api.chatwork.com/v2/rooms/281437593/messages"

    headers = {
        "x-chatworktoken": api_key
        }

    payload = "self_unread=1"

    total_qty = get_total_qty(yesterday)
    total_amount = get_total_amount(yesterday)

    body = render_template('daily-report.txt', now=now, yesterday=yesterday, total_qty=total_qty, total_amount=total_amount)

    params = { "body" : body }

    response = requests.post(url, headers=headers, data=payload, params=params)

    return ('', 204)
    # return body