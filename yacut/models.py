from datetime import datetime

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
