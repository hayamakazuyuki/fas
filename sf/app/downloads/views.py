from flask import Blueprint, render_template
from flask_login import login_required

downloads = Blueprint('downloads', __name__, url_prefix='/downloads')


@downloads.route('/')
@login_required
def index():
    return render_template('downloads/index.html')
