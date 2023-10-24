from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash
from flask_login import UserMixin
import secrets 

db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow())
    lists = db.relationship('CryptoList', backref='user', lazy=True)
    alerts = db.relationship('Alert', backref='user', lazy=True)

    def __init__(self, first_name, last_name, email, password):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = generate_password_hash(password)


class CryptoList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    cryptos = db.relationship('Crypto', backref='list', lazy=True)

    def __init__(self, name, user_id):
        self.name = name
        self.user_id = user_id


class Crypto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    symbol = db.Column(db.String, nullable=False)
    current_price = db.Column(db.Float, nullable=False)
    all_time_high_price = db.Column(db.Float, nullable=False)
    market_cap = db.Column(db.Float, nullable=False)
    list_id = db.Column(db.Integer, db.ForeignKey('crypto_list.id'), nullable=False)

    def __init__(self, name, symbol, current_price, all_time_high_price, market_cap, list_id):
        self.name = name
        self.symbol = symbol
        self.current_price = current_price
        self.all_time_high_price = all_time_high_price
        self.market_cap = market_cap
        self.list_id = list_id

class UserCrypto(db.Model):
    __tablename__ = 'user_crypto'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    crypto_id = db.Column(db.Integer, db.ForeignKey('crypto.id'), nullable=False)
    notes = db.Column(db.Text)

    user = db.relationship('User', backref=db.backref('user_cryptos', cascade='all, delete-orphan'))
    crypto = db.relationship('Crypto', backref=db.backref('user_cryptos', cascade='all, delete-orphan'))

    def __init__(self, user_id, crypto_id, notes=None):
        self.user_id = user_id
        self.crypto_id = crypto_id
        self.notes = notes




class Alert(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    crypto_name = db.Column(db.String, nullable=False)
    price = db.Column(db.Float, nullable=False)
    direction = db.Column(db.String, nullable=False)
    channel = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow())

    def __init__(self, crypto_name, price, direction, channel, user_id):
        self.crypto_name = crypto_name
        self.price = price
        self.direction = direction
        self.channel = channel
        self.user_id = user_id

class ResetRequest(db.Model):  
    id = db.Column(db.Integer, primary_key=True)
    secret_key = db.Column(db.String, unique=True, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __init__(self, secret_key, user_id):
        self.secret_key = secret_key
        self.user_id = user_id

        
