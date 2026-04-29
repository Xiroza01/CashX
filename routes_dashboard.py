import os
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename
from models import db, Transaction

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        current_user.name = request.form.get('name')
        new_pin = request.form.get('pin')
        pic_url = request.form.get('profile_pic')
        pic_file = request.files.get('profile_pic_file')
        bank_balance = request.form.get('bank_balance')
        
        if new_pin:
            current_user.pin_hash = generate_password_hash(new_pin, method='pbkdf2:sha256')
            
        if bank_balance is not None:
            try:
                new_balance = float(bank_balance)
                if current_user.linked_banks:
                    current_user.linked_banks[0].balance = new_balance
            except ValueError:
                pass
            
        if pic_file and pic_file.filename:
            filename = secure_filename(pic_file.filename)
            upload_folder = os.path.join('static', 'images')
            os.makedirs(upload_folder, exist_ok=True)
            filepath = os.path.join(upload_folder, filename)
            pic_file.save(filepath)
            current_user.profile_pic = f"/static/images/{filename}"
            
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

@dashboard_bp.route('/add_money', methods=['POST'])
@login_required
def add_money():
    amount_str = request.form.get('amount')
    try:
        amount = float(amount_str)
        if amount > 0:
            current_user.balance += amount
            # Create a transaction record
            tx = Transaction(
                user_id=current_user.id,
                amount=amount,
                type='credit',
                category='top-up',
                description='Wallet Top-up'
            )
            db.session.add(tx)
            db.session.commit()
            flash(f'Successfully added ₹{amount:.2f} to your wallet.', 'success')
        else:
            flash('Please enter a valid amount.', 'danger')
    except (ValueError, TypeError):
        flash('Invalid amount entered.', 'danger')
        
    return redirect(url_for('dashboard.home'))

import csv
from flask import Response

@dashboard_bp.route('/download_statement')
@login_required
def download_statement():
    format_type = request.args.get('format', 'csv')
    transactions = Transaction.query.filter_by(user_id=current_user.id).order_by(Transaction.timestamp.desc()).all()
    
    if format_type == 'pdf':
        return render_template('dashboard/statement_print.html', transactions=transactions)
        
    def generate_csv():
        yield 'Date,Transaction ID,Description,Category,Type,Status,Amount (INR)\n'
        for tx in transactions:
            amount_str = f"{abs(tx.amount):.2f}"
            row = [
                tx.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                f"TXN{tx.id:06d}",
                f'"{tx.description}"',
                tx.category.capitalize(),
                tx.type.capitalize(),
                tx.status.capitalize(),
                amount_str
            ]
            yield ','.join(row) + '\n'

    if format_type == 'excel':
        # Generate a simple HTML table that Excel can open
        def generate_excel():
            yield '<html><body><table border="1">'
            yield '<tr><th>Date</th><th>Transaction ID</th><th>Description</th><th>Category</th><th>Type</th><th>Status</th><th>Amount (INR)</th></tr>'
            for tx in transactions:
                amount_str = f"{abs(tx.amount):.2f}"
                yield f'<tr><td>{tx.timestamp.strftime("%Y-%m-%d %H:%M:%S")}</td><td>TXN{tx.id:06d}</td><td>{tx.description}</td><td>{tx.category.capitalize()}</td><td>{tx.type.capitalize()}</td><td>{tx.status.capitalize()}</td><td>{amount_str}</td></tr>'
            yield '</table></body></html>'
        
        return Response(generate_excel(), mimetype='application/vnd.ms-excel', headers={'Content-Disposition': 'attachment; filename=CashX_Statement.xls'})

    # Default CSV
    return Response(generate_csv(), mimetype='text/csv', headers={'Content-Disposition': 'attachment; filename=CashX_Statement.csv'})
