from flask import Blueprint
from flask_login import login_required

downloads = Blueprint('downloads', __name__, url_prefix='/downloads')


@downloads.route('/')
@login_required
def index():
    return 'dl'
