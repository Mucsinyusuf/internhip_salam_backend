from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from datetime import datetime

db = SQLAlchemy()

class Admin(db.Model):
    __tablename__ = 'admins'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)  # Store hashed passwords ideally


class Customer(db.Model, SerializerMixin):
    __tablename__ = 'customers'
    serialize_rules = ('-transactions.customer',)

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    phone = db.Column(db.String, unique=True, nullable=False)  # phone as string and unique
    account_status = db.Column(db.String, default='active')
    balance = db.Column(db.Float, default=0.0)

    transactions = db.relationship('Transaction', backref='customer', lazy=True)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
            "account_status": self.account_status,
            "balance": self.balance
        }


class Transaction(db.Model, SerializerMixin):
    __tablename__ = 'transactions'
    serialize_rules = ('-customer.transactions',)

    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String, nullable=False)  # e.g., 'deposit', 'withdrawal'
    amount = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "customer_name": self.customer.name,
            "type": self.type,
            "amount": self.amount,
            "timestamp": self.timestamp.isoformat()
        }
