from flask import Blueprint, render_template

from ..models import DeliveryRequest

delivery = Blueprint('delivery', __name__, url_prefix='/delivery')


@delivery.route('/')
def index():
    requests = DeliveryRequest.query.order_by(DeliveryRequest.id.desc()).limit(50).all()

    return render_template('delivery/index.html', requests=requests)
