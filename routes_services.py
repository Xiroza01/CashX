from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models import db, Transaction

services_bp = Blueprint('services', __name__)

@services_bp.route('/pay', methods=['GET', 'POST'])
@login_required
def pay():
    if request.method == 'POST':
        upi_id = request.form.get('upi_id')
        amount = float(request.form.get('amount') or 0)
        pin = request.form.get('pin')

        # In a real app we'd verify PIN against user.pin_hash here for transfer
        # For simulation, just deduct and record
        if amount > 0 and amount <= current_user.balance:
            current_user.balance -= amount
            tx = Transaction(user_id=current_user.id, amount=-amount, type='debit', category='payment', description=f"Paid to {upi_id}")
            db.session.add(tx)
            db.session.commit()
            flash(f'Payment of ₹{amount} to {upi_id} successful!', 'success')
            return redirect(url_for('dashboard.home'))
        else:
            flash('Insufficient balance or invalid amount.', 'danger')

    return render_template('services/payments.html')

@services_bp.route('/recharge', methods=['GET', 'POST'])
@login_required
def recharge():
    if request.method == 'POST':
        provider = request.form.get('provider')
        amount = float(request.form.get('amount') or 0)
        
        if amount > 0 and amount <= current_user.balance:
            current_user.balance -= amount
            tx = Transaction(user_id=current_user.id, amount=-amount, type='debit', category='recharge', description=f"{provider} Recharge")
            db.session.add(tx)
            db.session.commit()
            flash('Recharge successful!', 'success')
            return redirect(url_for('dashboard.home'))
        else:
            flash('Insufficient balance.', 'danger')

    return render_template('services/recharge.html')

@services_bp.route('/travel', methods=['GET', 'POST'])
@login_required
def travel():
    if request.method == 'POST':
        destination = request.form.get('destination')
        amount = 5000.0 # Mock flat rate
        if current_user.balance >= amount:
            current_user.balance -= amount
            tx = Transaction(user_id=current_user.id, amount=-amount, type='debit', category='travel', description=f"Booking to {destination}")
            db.session.add(tx)
            db.session.commit()
            flash(f'Booking to {destination} confirmed!', 'success')
            return redirect(url_for('dashboard.home'))
        else:
            flash('Insufficient balance for booking.', 'danger')
            
    return render_template('services/travel.html')

@services_bp.route('/invest', methods=['GET', 'POST'])
@login_required
def invest():
    gold_price_per_gram = 6500.0
    if request.method == 'POST':
        amount = float(request.form.get('amount') or 0)
        grams = amount / gold_price_per_gram
        
        if amount > 0 and amount <= current_user.balance:
            current_user.balance -= amount
            current_user.gold_balance_grams += grams
            tx = Transaction(user_id=current_user.id, amount=-amount, type='debit', category='investment', description=f"Bought {round(grams, 4)}g Digital Gold")
            db.session.add(tx)
            db.session.commit()
            flash('Gold purchase successful!', 'success')
            return redirect(url_for('dashboard.home'))
        else:
            flash('Insufficient wallet balance.', 'danger')

    return render_template('services/invest.html', price=gold_price_per_gram)
