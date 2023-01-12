from flask import Blueprint, render_template
import datetime
import requests
import os

scheduled = Blueprint('scheduled', __name__)

JST = datetime.timezone(datetime.timedelta(hours=+9), 'JST')
now = datetime.datetime.now(JST)


@scheduled.route('/daily-report')
def daily_report():

    api_key = os.environ.get('X_CHATWORK_TOKEN')
    url = "https://api.chatwork.com/v2/rooms/281437593/messages"
    body = render_template('daily-report.txt', now=now)
    payload = "self_unread=1"

    headers = {
        "x-chatworktoken": api_key
        }

    params = { "body" : body }

    response = requests.post(url, headers=headers, data=payload, params=params)

    return ('', 204)