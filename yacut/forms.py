from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import DataRequired, Length, Optional


URL_LENGTH = 16


class URLMapForm(FlaskForm):
    original_link = URLField(
        'Введите ссылку',
        validators=[DataRequired(message='Обязательное поле')])
    custom_id = StringField(
        'Введите свой вариант короткой ссылки',
        validators=[Length(0, URL_LENGTH), Optional()]
    )
    create = SubmitField('Создать')
