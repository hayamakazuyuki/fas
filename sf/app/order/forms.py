from flask_wtf import FlaskForm
from wtforms import IntegerField, DateField, SelectField
from wtforms.validators import InputRequired, NumberRange, Optional

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
    delivery_date = DateField('指定日', [Optional()])
    time_range = SelectField('時間帯', choices=[('', ''), ('am', '午前'), ('pm', '午後')])
    

"""
class OrderInputForm(FlaskForm):
    item = SelectField('商品',
    choices=[('', '----- 半透明 -----'), ('602', '45L'), ('622', '45L-200枚'), ('629', '45L-50枚x10箱'), 
    ('603', '70L'), ('651', '70L（100枚x5）'), ('627', '70L（0.05mm）'), ('604', '90L'), ('626', '90L（0.05mm）'), 
    ('605', '120L'), ('623', '150L'), ('628', 'Pカバー（40枚入）'), ('680', '再生材ごみ袋（1500x2000）'), ('606', '（青色）45L'), ('624', '（青色）45L-200枚'), 
    ('607', '（青色）70L'), ('608', '（青色）90L'), ('609', '（黄色）45L'), ('625', '（黄色）45L-200枚'), ('610', '（黄色）70L'), 
    ('611', '（黄色）90L')],
        validators=[DataRequired('商品を選択して下さい。')])
    price = IntegerField('単価', validators=[DataRequired('単価を入力して下さい。')])
    qty = IntegerField('数量', validators=[DataRequired('数量を入力して下さい。'),
                                             NumberRange(min=1, message='数量は１以上を入力して下さい。')])

class OrderInputForm2(FlaskForm):
    item2 = SelectField('商品',
    choices=[('', '----- 半透明 -----'), ('602', '45L'), ('622', '45L-200枚'), ('629', '45L-50枚x10箱'), 
    ('603', '70L'), ('651', '70L（100枚x5）'), ('627', '70L（0.05mm）'), ('604', '90L'), ('626', '90L（0.05mm）'), 
    ('605', '120L'), ('623', '150L'), ('628', 'Pカバー（40枚入）'), ('680', '再生材ごみ袋（1500x2000）'), ('606', '（青色）45L'), ('624', '（青色）45L-200枚'), 
    ('607', '（青色）70L'), ('608', '（青色）90L'), ('609', '（黄色）45L'), ('625', '（黄色）45L-200枚'), ('610', '（黄色）70L'), 
    ('611', '（黄色）90L')],
        validators=[DataRequired('商品を選択して下さい。')])
    price2 = IntegerField('単価', validators=[DataRequired('単価を入力して下さい。')])
    qty2 = IntegerField('数量', validators=[DataRequired('数量を入力して下さい。'),
                                             NumberRange(min=1, message='数量は１以上を入力して下さい。')])
class OrderInputForm3(FlaskForm):
    item3 = SelectField('商品',
    choices=[('', '----- 半透明 -----'), ('602', '45L'), ('622', '45L-200枚'), ('629', '45L-50枚x10箱'), 
    ('603', '70L'), ('651', '70L（100枚x5）'), ('627', '70L（0.05mm）'), ('604', '90L'), ('626', '90L（0.05mm）'), 
    ('605', '120L'), ('623', '150L'), ('628', 'Pカバー（40枚入）'), ('680', '再生材ごみ袋（1500x2000）'), ('606', '（青色）45L'), ('624', '（青色）45L-200枚'), 
    ('607', '（青色）70L'), ('608', '（青色）90L'), ('609', '（黄色）45L'), ('625', '（黄色）45L-200枚'), ('610', '（黄色）70L'), 
    ('611', '（黄色）90L')],
        validators=[DataRequired('商品を選択して下さい。')])
    price3 = IntegerField('単価', validators=[DataRequired('単価を入力して下さい。')])
    qty3 = IntegerField('数量', validators=[DataRequired('数量を入力して下さい。'),
                                             NumberRange(min=1, message='数量は１以上を入力して下さい。')])


class OrderInputFormD(FlaskForm):
    itemD = HiddenField('送料', validators=[DataRequired('')])
    priceD = IntegerField('送料単価', validators=[DataRequired('単価を入力して下さい。')])
    qtyD = IntegerField('数量', validators=[DataRequired('数量を入力して下さい。'),
                                            NumberRange(min=1, message='数量は１以上を入力して下さい。')])

"""