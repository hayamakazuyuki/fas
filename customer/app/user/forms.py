from flask_wtf import FlaskForm

from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired


class LoginForm(FlaskForm):
    email = StringField('メールアドレス', validators=[InputRequired('メールアドレスを入力して下さい。')])
    password = PasswordField('パスワード', validators=[InputRequired('パスワードを入力してください。')])

