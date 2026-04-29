from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models import db, Transaction

services_bp = Blueprint('services', __name__)

def detect_category(upi_id):
    if not upi_id:
        return 'payment'
    upi_lower = upi_id.lower()
    if any(k in upi_lower for k in ['zomato', 'swiggy', 'food', 'kfc', 'mcd', 'restaurant']):
        return 'food'
    if any(k in upi_lower for k in ['amazon', 'flipkart', 'myntra', 'shop', 'store', 'mart', 'supermarket']):
        return 'shopping'
    if any(k in upi_lower for k in ['bescom', 'electricity', 'water', 'gas', 'bill', 'utility']):
        return 'bills'
    if any(k in upi_lower for k in ['jio', 'airtel', 'vi', 'recharge', 'dth', 'broadband']):
        return 'recharge'
    if any(k in upi_lower for k in ['uber', 'ola', 'taxi', 'cab', 'travel', 'flight', 'irctc']):
        return 'travel'
    return 'payment'

@services_bp.route('/pay', methods=['GET', 'POST'])
@login_required
def pay():
    if request.method == 'POST':
        upi_id = request.form.get('upi_id')
        amount = float(request.form.get('amount') or 0)
        pin = request.form.get('pin')
        category_choice = request.form.get('category')

        # In a real app we'd verify PIN against user.pin_hash here for transfer
        # For simulation, just deduct and record
        if amount > 0 and amount <= current_user.balance:
            current_user.balance -= amount
            if category_choice and category_choice != 'auto':
                assigned_cat = category_choice
            else:
                assigned_cat = detect_category(upi_id)
                
            tx = Transaction(user_id=current_user.id, amount=-amount, type='debit', category=assigned_cat, description=f"Paid to {upi_id}")
            db.session.add(tx)
            db.session.commit()
            flash(f'Payment of ₹{amount} to {upi_id} successful! Category: {assigned_cat.capitalize()}', 'success')
            return redirect(url_for('dashboard.home'))
        else:
            flash('Insufficient balance or invalid amount.', 'danger')

    return render_template('services/payments.html')

@services_bp.route('/recharge', methods=['GET', 'POST'])
@login_required
def recharge():
    if request.method == 'POST':
        provider = request.form.get('provider')
        biller_type = request.form.get('biller_type', 'mobile')
        amount = float(request.form.get('amount') or 0)
        
        if biller_type == 'electricity':
            category = 'bills'
            desc = f"Electricity Bill ({provider})"
        elif biller_type == 'fastag':
            category = 'travel'
            desc = f"Fastag Recharge ({provider})"
        elif biller_type == 'dth':
            category = 'recharge'
            desc = f"DTH Recharge ({provider})"
        else:
            category = 'recharge'
            desc = f"Mobile Recharge ({provider})"
        
        if amount > 0 and amount <= current_user.balance:
            current_user.balance -= amount
            tx = Transaction(user_id=current_user.id, amount=-amount, type='debit', category=category, description=desc)
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
        booking_type = request.form.get('booking_type', 'Flights')
        destination = request.form.get('destination')
        amount = 5000.0 # Mock flat rate
        
        category = 'travel'
        if booking_type == 'Movies':
            category = 'movies'
            desc = f"Movie Ticket: {destination}"
        else:
            desc = f"{booking_type} Booking to {destination}"
            
        if current_user.balance >= amount:
            current_user.balance -= amount
            tx = Transaction(user_id=current_user.id, amount=-amount, type='debit', category=category, description=desc)
            db.session.add(tx)
            db.session.commit()
            flash(f'Confirmed: {desc}!', 'success')
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
