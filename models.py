from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=True)
    phone_number = db.Column(db.String(15), unique=True, nullable=False)
    upi_id = db.Column(db.String(50), unique=True, nullable=True)
    pin_hash = db.Column(db.String(255), nullable=False)
    profile_pic = db.Column(db.String(255), default='https://ui-avatars.com/api/?name=User&background=random')
    otp_consent = db.Column(db.Boolean, default=False)
    balance = db.Column(db.Float, default=5000.0) # Mock starting balance
    gold_balance_grams = db.Column(db.Float, default=0.0)
    
    transactions = db.relationship('Transaction', backref='user', lazy=True)
    linked_banks = db.relationship('BankAccount', backref='user', lazy=True)

class BankAccount(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    bank_name = db.Column(db.String(100), nullable=False)
    account_number_last4 = db.Column(db.String(4), nullable=False)
    balance = db.Column(db.Float, default=10000.0)

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    type = db.Column(db.String(20), nullable=False) # 'credit', 'debit'
    category = db.Column(db.String(50), nullable=False) # 'payment', 'recharge', 'travel', 'investment'
    description = db.Column(db.String(255), nullable=True)
    status = db.Column(db.String(20), default='completed') # completed, pending, failed
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
