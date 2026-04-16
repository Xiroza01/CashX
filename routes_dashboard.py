from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash
from models import db, Transaction

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        current_user.name = request.form.get('name')
        new_pin = request.form.get('pin')
        pic_url = request.form.get('profile_pic')
        
        if new_pin:
            current_user.pin_hash = generate_password_hash(new_pin)
        if pic_url:
            current_user.profile_pic = pic_url
            
        db.session.commit()
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('dashboard.profile'))
        
    return render_template('dashboard/profile.html')

@dashboard_bp.route('/dashboard')
@login_required
def home():
    recent_transactions = Transaction.query.filter_by(user_id=current_user.id).order_by(Transaction.timestamp.desc()).limit(5).all()
    # Calculate total bank balance
    bank_balance = sum([b.balance for b in current_user.linked_banks])
    
    return render_template('dashboard/index.html', transactions=recent_transactions, bank_balance=bank_balance)

@dashboard_bp.route('/passbook')
@login_required
def passbook():
    all_transactions = Transaction.query.filter_by(user_id=current_user.id).order_by(Transaction.timestamp.desc()).all()
    return render_template('dashboard/passbook.html', transactions=all_transactions)
