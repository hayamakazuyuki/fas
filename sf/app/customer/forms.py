from random import choices
from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, SelectField
from wtforms.validators import InputRequired, NumberRange, Length, Regexp
# from wtforms_sqlalchemy.fields import QuerySelectField

from ..models import Staff


# def staff_query():
#     return Staff.query.filter(Staff.is_inactive==False)


# class CustomerForm(FlaskForm):
#     id = IntegerField('取引先ID', validators=[InputRequired('IDは必須です。'),
#                                            NumberRange(min=1, max=99999, message='IDは最大5桁です。')])
#     name = StringField('取引先名', validators=[InputRequired('取引先名を入力して下さい。')])
#     staff = QuerySelectField('営業担当', query_factory=staff_query, allow_blank=True, get_label='last_name')

#     def validate_staff(form, field):
#         if field.data is None:
#             raise ValidationError('営業担当者を選択して下さい。')


class CustomerRegisterForm(FlaskForm):
    id = IntegerField('取引先ID', validators=[InputRequired('IDは必須です。'),
                                           NumberRange(min=1, max=99999, message='IDは最大5桁です。')])
    name = StringField('取引先名', validators=[InputRequired('取引先名を入力して下さい。')])
    staff = SelectField('営業担当', validators=[InputRequired('営業担当者を入力してください。')])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._set_staffs()

    def _set_staffs(self):
        staffs = Staff.query.filter(Staff.is_inactive==False).all()
        # set staffs from db as tuple(value, text)
        self.staff.choices = [('', '')]+[(staff.id, staff.last_name + staff.first_name) for staff in staffs]


# def customer_edit_form(current_staff):
#     class CustomerEditForm(FlaskForm):
#         id = IntegerField('取引先ID', validators=[InputRequired('IDは必須です。'),
#                                            NumberRange(min=1, max=99999, message='IDは最大5桁です。')])
#         name = StringField('取引先名', validators=[InputRequired('取引先名を入力して下さい。')])
#         staff = QuerySelectField('営業担当', query_factory=staff_query, get_label='last_name',
#             default=lambda: Staff.query.filter(Staff.id==current_staff).one_or_none())

#     return CustomerEditForm


class ShopForm(FlaskForm):
    id = IntegerField('事業所ID', validators=[InputRequired('事業所IDを入力して下さい。'),
                                           NumberRange(min=1, max=99999, message='IDは最大5桁です')])
    shop_number = StringField('顧客の事業所番号')
    name = StringField('事業所名', validators=[InputRequired()])
    department = StringField('部署/担当')
    zip = StringField('郵便番号', validators=[InputRequired('郵便番号を入力して下さい。'),
                                          Length(min=7, max=7, message='郵便番号は7桁です'),
                                          Regexp('[0-9]+', message='半角数字のみで7桁です')])
    prefecture = StringField('都道府県', validators=[InputRequired('都道府県を入力して下さい。')])
    city = StringField('市区町村', validators=[InputRequired('市区町村を入力して下さい。')])
    town = StringField('町域', validators=[InputRequired('町域を入力して下さい。')])
    address = StringField('番地', validators=[InputRequired('番地以下を入力して下さい。')])
    building = StringField('建物名他')
    telephone = StringField('電話番号', validators=[InputRequired('電話番号を入力して下さい。'),
                                                Regexp('[0-9]+-[0-9]+-[0-9]+', message='数字-数字-数字です。')])
