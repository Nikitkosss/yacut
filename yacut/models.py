from datetime import datetime
from sqlalchemy.orm import validates
from .error_handlers import InvalidAPIUsage
import re

from . import db

URL = 'http://localhost/'


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String, nullable=False)
    short = db.Column(db.String(16), unique=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def to_dict(self):
        return dict(
            url=self.original,
            short_link=URL + self.short
        )

    def from_dict(self, data):
        for field in ['original', 'short']:
            if field in data:
                setattr(self, field, data[field])

    @validates('original')
    def validate_original(self, key, value):
        if not value:
            raise InvalidAPIUsage('\"url\" является обязательным полем!')
        return value

    @validates('short')
    def validate_short(self, key, value):
        if URLMap.query.filter_by(short=value).first():
            raise InvalidAPIUsage(
                'Предложенный вариант короткой ссылки уже существует.'
            )

        correct = re.match("""^[a-zA-z0-9]{0,16}$""", value)
        if not correct:
            raise InvalidAPIUsage(
                'Указано недопустимое имя для короткой ссылки'
            )
        return value
