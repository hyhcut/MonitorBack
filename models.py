from ext import db
from werkzeug.security import generate_password_hash, check_password_hash
# from flask_login import UserMixin


def to_dict(self):
    return {c.name: getattr(self, c.name, None) for c in self.__table__.columns}

def init(self, dict):
    for key, value in dict.items():
        if hasattr(self, key):
            if key == "password":
                self.set_password(value)
            else:
                setattr(self, key, value)


db.Model.to_dict = to_dict
db.Model.__init__ = init


class User(db.Model):
    __tablename__ = 't_user'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=True)
    power_id = db.Column(db.Integer, db.ForeignKey('d_power.code'))
    last_time = db.Column(db.DateTime)
    power = db.relationship("DictPower", uselist=False, lazy="joined")

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def list_show(self):
        return {
            'id': self.id,
            'username': self.username,
            'power_id': self.power_id,
            'power': self.power.name,
            'last_time': self.last_time.strftime("%Y-%m-%d %H:%M:%S") if self.last_time else ""
        }


class DictPower(db.Model):
    __tablename__ = 'd_power'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    code = db.Column(db.Integer, unique=True, nullable=False)
    name = db.Column(db.String(255))

    def select_show(self):
        return {
            'label': self.name,
            'value': self.code
        }


class DictServerType(db.Model):
    __tablename__ = 'd_server_type'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(100), unique=True)

    def select_show(self):
        return {
            'label': self.name,
            'value': self.id
        }


class Server(db.Model):
    __tablename__ = 't_server'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    type_id = db.Column(db.Integer, db.ForeignKey('d_server_type.id'))
    address = db.Column(db.String(100))
    username = db.Column(db.String(100))
    password = db.Column(db.String(100))
    note = db.Column(db.Text)
    server_type = db.relationship("DictServerType", uselist=False, lazy="joined")

    def __init__(self, dict):
        for key, value in dict.items():
            if hasattr(self, key):
                setattr(self, key, value)

    def list_show(self):
        return {
            'id': self.id,
            'name': self.name,
            'type': self.server_type.name,
            'type_id': self.type_id,
            'address': self.address,
            'username': self.username,
            'password': self.password
        }