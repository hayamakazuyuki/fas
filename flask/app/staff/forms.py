from flask_wtf import FlaskForm

from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Email

class LoginForm(FlaskForm):
    email = StringField('メールアドレス', validators=[InputRequired('メールアドレスは必須です。'), 
        Email('ログイン情報をご確認ください。')])
    password = PasswordField('パスワード', validators=[InputRequired('パスワードを入力してください。')])
