from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from datetime import datetime

db = SQLAlchemy()

class Admin(db.Model):
    __tablename__ = 'admins'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)  # Ideally store hashed passwords


class Customer(db.Model, SerializerMixin):
    __tablename__ = 'customers'
    serialize_rules = ('-transactions.customer',)

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    phone = db.Column(db.String, unique=True, nullable=False)
    account_status = db.Column(db.String, default='active')
    balance = db.Column(db.Float, default=0.0)

    # Relationship to transactions
    transactions = db.relationship(
        'Transaction',
        back_populates='customer',
        cascade='all, delete-orphan',
        passive_deletes=True,
        lazy=True
    )

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
    type = db.Column(db.String, nullable=False)
    amount = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id', ondelete='CASCADE'), nullable=False)

    # Add the missing back_populates relationship
    customer = db.relationship('Customer', back_populates='transactions')

    def to_dict(self):
        return {
            "id": self.id,
            "customer_name": self.customer.name if self.customer else "Unknown",
            "type": self.type,
            "amount": self.amount,
            "timestamp": self.timestamp.isoformat()
        }
