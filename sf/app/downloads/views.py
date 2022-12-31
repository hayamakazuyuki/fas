from flask import Blueprint, render_template, request
from flask_login import login_required
import datetime

downloads = Blueprint('downloads', __name__, url_prefix='/downloads')
JST = datetime.timezone(datetime.timedelta(hours=+9), 'JST')


@downloads.route('/')
@login_required
def index():
    target = request.args.get("target")

    if target is None:
        target = datetime.datetime.now(JST)

    return render_template('downloads/index.html', target=target)
