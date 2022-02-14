from flask_wtf import FlaskForm

from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Email

class LoginForm(FlaskForm):
    email = StringField('メールアドレス', validators=[InputRequired('メールアドレスは必須です。'), 
        Email('正しいメールアドレスを入力してください。')])
    password = PasswordField('パスワード', validators=[InputRequired('パスワードを入力してください。')])
    