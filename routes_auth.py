from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User, BankAccount

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.home'))

    if request.method == 'POST':
        phone = request.form.get('phone_number')
        pin = request.form.get('pin')

        user = User.query.filter_by(phone_number=phone).first()
        if user and check_password_hash(user.pin_hash, pin):
            login_user(user)
            return redirect(url_for('dashboard.home'))
        
        flash('Invalid phone number or PIN.', 'danger')

    return render_template('auth/login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.home'))

    if request.method == 'POST':
        name = request.form.get('name')
        phone = request.form.get('phone_number')
        pin = request.form.get('pin')

        # Basic check
        existing = User.query.filter_by(phone_number=phone).first()
        if existing:
            flash('Account already exists.', 'warning')
            return redirect(url_for('auth.login'))

        # Create user
        upi_id = f"{phone}@cashx"
        hashed_pin = generate_password_hash(pin)
        new_user = User(name=name, phone_number=phone, upi_id=upi_id, pin_hash=hashed_pin)
        db.session.add(new_user)
        db.session.commit()

        # Link a default mock bank account
        bank = BankAccount(user_id=new_user.id, bank_name="CashX Payments Bank", account_number_last4="1234", balance=15000)
        db.session.add(bank)
        db.session.commit()

        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('auth/register.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
