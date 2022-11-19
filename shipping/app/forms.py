from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from wtforms.validators import InputRequired


class FileUploadForm(FlaskForm):
    file = FileField('ファイル', validators=[InputRequired('csvファイルを選択して下さい。')])
    submit = SubmitField('登録')
