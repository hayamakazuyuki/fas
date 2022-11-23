from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms import SubmitField


class FileUploadForm(FlaskForm):
    file = FileField('ファイル', validators=[FileRequired('csvファイルを選択して下さい。')])
    submit = SubmitField('登録')
