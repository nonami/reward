from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class VoucherType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Float)
    order_lower_bound = db.Column(db.Float)
    order_upper_bound = db.Column(db.Float,  default=0)
    validity = db.Column(db.Integer)

    def __str__(self):
        return f"{self.value}: {self.order_lower_bound} - {self.order_upper_bound}: {self.validity} days"


class Voucher(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, unique=True)
    voucher_code = db.Column(db.String(20), unique=True)
    voucher_type_id = db.Column(db.Integer, db.ForeignKey('voucher_type.id'))
    voucher_type = db.relationship('VoucherType', lazy=True)
    created_at = db.Column(db.DateTime) # default to today
    activated = db.Column(db.Boolean, default=False)
    used = db.Column(db.Boolean, default=False)
    expire_at = db.Column(db.DateTime)

    @property
    def is_useable(self):
        return self.activated and not self.used and self.expire_at > datetime.utcnow()

    def to_dict(self):
        return {
            'code': self.voucher_code,
            'amount': self.voucher_type.value,
            'expires': self.expire_at.strftime("%Y-%m-%d %H:%m:%S"),
            'is_useable': self.is_useable
        }


class AppUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean, default=True)