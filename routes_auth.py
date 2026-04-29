from flask import Blueprint, render_template, request, redirect, url_for, flash, session
import random
import threading
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User, BankAccount

auth_bp = Blueprint('auth', __name__)

def send_otp_helper(identifier, otp):
    # Simulated OTP Sending fallback
    print(f"[{identifier}] OTP generated: {otp}")
    
    is_email = '@' in identifier
    try:
        if is_email:
            import smtplib
            from email.mime.text import MIMEText
            from email.mime.multipart import MIMEMultipart
            import os
            
            sender_email = os.environ.get('EMAIL_USER')
            sender_password = os.environ.get('EMAIL_PASS')
            
            if sender_email and sender_password and sender_email != 'your_email@gmail.com':
                msg = MIMEMultipart()
                msg['From'] = sender_email
                msg['To'] = identifier
                msg['Subject'] = "CashX OTP Code"
                body = f"Your CashX OTP is: {otp}. It is valid for a short time."
                msg.attach(MIMEText(body, 'plain'))
                
                server = smtplib.SMTP('smtp.gmail.com', 587)
                server.starttls()
                server.login(sender_email, sender_password)
                server.send_message(msg)
                server.quit()
                print(f"Successfully sent OTP email to {identifier}")
            else:
                print("⚠️  EMAIL_USER is not set to a real email in .env! Skipping real email.")
                
        else:
            # Phone number (SMS)
            import os
            from twilio.rest import Client
            
            account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
            auth_token = os.environ.get('TWILIO_AUTH_TOKEN')
            twilio_number = os.environ.get('TWILIO_PHONE_NUMBER')
            
            if account_sid and auth_token and twilio_number and account_sid != 'your_account_sid':
                client = Client(account_sid, auth_token)
                message = client.messages.create(
                    body=f"Your CashX OTP is: {otp}",
                    from_=twilio_number,
                    to=identifier
                )
                print(f"Successfully sent SMS to {identifier}, SID: {message.sid}")
            else:
                print("⚠️  Twilio credentials not set to real values in .env! Skipping real SMS.")
    except Exception as e:
        print(f"Failed to send real OTP: {e}")

def check_placeholder_creds(identifier):
    """Helper to check if real credentials exist, returns True if using placeholders"""
    import os
    is_email = '@' in identifier
    if is_email:
        email = os.environ.get('EMAIL_USER', '')
        return not email or email == 'your_email@gmail.com'
    else:
        sid = os.environ.get('TWILIO_ACCOUNT_SID', '')
        return not sid or sid == 'your_account_sid'

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.home'))

    if request.method == 'POST':
        identifier = request.form.get('identifier', '').strip()
        
        user = User.query.filter((User.phone_number == identifier) | (User.email == identifier)).first()
        if user:
            # Generate 6-digit OTP
            otp = str(random.randint(100000, 999999))
            
            # Store user ID and OTP in session temporarily
            session['otp'] = otp
            session['pending_user_id'] = user.id
            session['auth_method'] = identifier
            session['auth_action'] = 'login'
            
            threading.Thread(target=send_otp_helper, args=(identifier, otp)).start()
                
            if check_placeholder_creds(identifier):
                flash(f"DEV MODE: Your OTP is {otp} (Add real credentials to .env to receive this via {'email' if '@' in identifier else 'SMS'})", "info")
            else:
                flash(f"An OTP has been sent to {identifier}.", "info")
                
            return redirect(url_for('auth.verify_otp'))
            
        flash('No account found with that phone number or email.', 'danger')

    return render_template('auth/login.html')

@auth_bp.route('/verify_otp', methods=['GET', 'POST'])
def verify_otp():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.home'))
        
    if 'otp' not in session:
        flash("Session expired. Please start over.", "warning")
        return redirect(url_for('auth.login'))
        
    if request.method == 'POST':
        entered_otp = request.form.get('otp')
        
        if entered_otp and entered_otp.strip() == session.get('otp'):
            action = session.get('auth_action')
            
            if action == 'login':
                user = User.query.get(session.get('pending_user_id'))
                if user:
                    login_user(user)
                    session.pop('otp', None)
                    session.pop('pending_user_id', None)
                    session.pop('auth_method', None)
                    session.pop('auth_action', None)
                    return redirect(url_for('dashboard.home'))
            
            elif action == 'register':
                # Create the user now
                reg_data = session.get('reg_data')
                upi_id = f"{reg_data['phone']}@cashx"
                hashed_pin = generate_password_hash('0000', method='pbkdf2:sha256') # Default PIN, no longer used for login
                
                new_user = User(
                    name=reg_data['name'], 
                    email=reg_data.get('email'), 
                    phone_number=reg_data['phone'], 
                    upi_id=upi_id, 
                    pin_hash=hashed_pin
                )
                db.session.add(new_user)
                db.session.commit()

                # Link a default mock bank account
                bank = BankAccount(user_id=new_user.id, bank_name="CashX Payments Bank", account_number_last4="1234", balance=15000)
                db.session.add(bank)
                db.session.commit()
                
                login_user(new_user)
                
                session.pop('otp', None)
                session.pop('reg_data', None)
                session.pop('auth_method', None)
                session.pop('auth_action', None)
                
                flash('Registration successful!', 'success')
                return redirect(url_for('dashboard.home'))
                
        flash('Invalid OTP. Please try again.', 'danger')
        
    method = session.get('auth_method', 'number/email')
    return render_template('auth/verify_otp.html', method=method)

@auth_bp.route('/resend_otp')
def resend_otp():
    if 'auth_method' not in session or 'auth_action' not in session:
        flash("Session expired. Please start over.", "warning")
        return redirect(url_for('auth.login'))
        
    identifier = session.get('auth_method')
    otp = str(random.randint(100000, 999999))
    session['otp'] = otp
    
    threading.Thread(target=send_otp_helper, args=(identifier, otp)).start()
    
    if check_placeholder_creds(identifier):
        flash(f"DEV MODE: Your new OTP is {otp} (Add real credentials to .env to receive this via {'email' if '@' in identifier else 'SMS'})", "info")
    else:
        flash(f"A new OTP has been sent to {identifier}.", "info")
        
    return redirect(url_for('auth.verify_otp'))

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.home'))

    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        phone = request.form.get('phone_number', '').strip()

        # Basic check
        existing = User.query.filter_by(phone_number=phone).first()
        if existing:
            flash('Account already exists with that phone number.', 'warning')
            return redirect(url_for('auth.login'))
            
        if email:
            existing_email = User.query.filter_by(email=email).first()
            if existing_email:
                flash('Account already exists with that email address.', 'warning')
                return redirect(url_for('auth.login'))

        # Prepare for OTP verification
        otp = str(random.randint(100000, 999999))
        session['otp'] = otp
        session['auth_action'] = 'register'
        
        # Decide where to send OTP (prefer email if provided)
        identifier = email if email else phone
        session['auth_method'] = identifier
        session['reg_data'] = {
            'name': name,
            'email': email,
            'phone': phone
        }
        
        threading.Thread(target=send_otp_helper, args=(identifier, otp)).start()
        
        if check_placeholder_creds(identifier):
            flash(f"DEV MODE: Your OTP is {otp} (Add real credentials to .env to receive this via {'email' if '@' in identifier else 'SMS'})", "info")
        else:
            flash(f"An OTP has been sent to {identifier} to complete registration.", "info")
            
        return redirect(url_for('auth.verify_otp'))

    return render_template('auth/register.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
