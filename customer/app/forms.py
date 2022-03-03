from flask_wtf import FlaskForm
from wtforms import SelectField
from wtforms_sqlalchemy.fields import QuerySelectField

from .models import DisplayProduct


def choice_query():
    return DisplayProduct.query

class CustomerOrderForm(FlaskForm):
    item = QuerySelectField('商品', query_factory=choice_query, allow_blank=True)
    qty = SelectField('数量', choices=[('1箱', '1'), ('2箱', '2'), ('3箱', '3'), ('4箱', '4'), ('5箱', '5')])