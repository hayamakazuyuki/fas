from flask import Blueprint
import datetime

scheduled = Blueprint('scheduled', __name__)

JST = datetime.timezone(datetime.timedelta(hours=+9), 'JST')
now = datetime.datetime.now(JST)

@scheduled.route('/daily-report')
def daily_report():
    
    return 'レポート'
