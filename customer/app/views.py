from flask import Blueprint

cs = Blueprint('cs', __name__)


@cs.route('/')
def index():
    return 'index'