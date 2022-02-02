from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField
from wtforms.validators import InputRequired, NumberRange

class CustomerForm(FlaskForm):
    id = IntegerField('取引先ID', validators=[InputRequired('IDは必須です。'),
                                           NumberRange(min=1, max=99999, message='IDは最大5桁です。')])
    name = StringField('取引先名', validators=[InputRequired('取引先名を入力して下さい。')])
