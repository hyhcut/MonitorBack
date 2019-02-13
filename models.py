from ext import db
from werkzeug.security import generate_password_hash, check_password_hash
# from flask_login import UserMixin


def to_dict(self):
    return {c.name: getattr(self, c.name, None) for c in self.__table__.columns}


db.Model.to_dict = to_dict


class User(db.Model):
    __tablename__ = 't_user'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=True)
    power = db.Column(db.Integer, nullable=False)
    last_time = db.Column(db.DateTime)

    def __init__(self, dict):
        for key, value in dict.items():
            if hasattr(self, key):
                if key == "password":
                    self.set_password(value)
                else:
                    setattr(self, key, value)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)