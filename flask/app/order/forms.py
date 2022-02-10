from flask_wtf import FlaskForm
from wtforms import IntegerField, DateField, StringField
from wtforms.validators import InputRequired, NumberRange

from wtforms_sqlalchemy.fields import QuerySelectField

from ..models import Product

def product_query():
    return Product.query


def order_edit_form(current_item):
    
    class OrderEditForm(FlaskForm):
        item = QuerySelectField('商品', query_factory=product_query, allow_blank=False, get_label='name',
                                default=lambda: Product.query.filter_by(id=current_item).one())
        price = IntegerField('単価', validators=[InputRequired('単価を入力してください')])
        qty = IntegerField('数量', validators=[InputRequired('数量を入力してください'),
                                             NumberRange(min=1, message='数量は 1 以上を入力してください')])
    return OrderEditForm

class DeliveryRequestForm(FlaskForm):
    delivery_date = DateField('指定日')
    memo = StringField('依頼事項')