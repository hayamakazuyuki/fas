from flask import Blueprint, render_template

from ..models import DeliveryRequest

shipping = Blueprint('shipping', __name__, url_prefix='/shipping')


@shipping.route('/')
def index():
    requests = DeliveryRequest.query.order_by(DeliveryRequest.id.desc()).limit(50).all()

    return render_template('shipping/index.html', requests=requests)
