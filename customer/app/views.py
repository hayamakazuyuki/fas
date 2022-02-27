from flask import Blueprint, render_template
from flask_login import login_required

cs = Blueprint('cs', __name__)


@cs.route('/')
@login_required
def index():
    return render_template('index.html')