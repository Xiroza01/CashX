from flask import Blueprint, render_template, request, redirect, url_for, flash, session
import random
import threading
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User, BankAccount

auth_bp = Blueprint('auth', __name__)

def send_otp_helper(identifier, otp):
    import os
    if '@' in identifier:
        # Email Delivery
        import smtplib
        from email.mime.text import MIMEText
        from email.mime.multipart import MIMEMultipart
        
        email_user = os.environ.get('EMAIL_USER')
        email_pass = os.environ.get('EMAIL_PASS')
        
        if email_user and email_pass and email_user != 'your_email@gmail.com':
            try:
                msg = MIMEMultipart()
                msg['From'] = email_user
                msg['To'] = identifier
                msg['Subject'] = "Your CashX Verification OTP"
                body = f"Your CashX Verification OTP is {otp}. Please do not share this code with anyone."
                msg.attach(MIMEText(body, 'plain'))
                
                server = smtplib.SMTP('smtp.gmail.com', 587)
                server.starttls()
                server.login(email_user, email_pass)
                server.send_message(msg)
                server.quit()
                print(f"[{identifier}] Email OTP sent successfully.")
            except Exception as e:
                print(f"[{identifier}] Failed to send Email OTP: {e}")
        else:
            print(f"[{identifier}] Email credentials not configured. Add EMAIL_USER and EMAIL_PASS to .env.")
            
    else:
        # SMS Delivery
        from twilio.rest import Client
        account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
        auth_token = os.environ.get('TWILIO_AUTH_TOKEN')
        from_phone = os.environ.get('TWILIO_PHONE_NUMBER')
        
        if account_sid and auth_token and from_phone and account_sid != 'your_account_sid':
            try:
                client = Client(account_sid, auth_token)
                message = client.messages.create(
                    body=f"Your CashX Verification OTP is {otp}. Do not share this code.",
                    from_=from_phone,
                    to=identifier
                )
                print(f"[{identifier}] SMS OTP sent successfully. SID: {message.sid}")
            except Exception as e:
                print(f"[{identifier}] Failed to send SMS OTP: {e}")
        else:
            print(f"[{identifier}] Twilio SMS credentials not configured in .env.")

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.home'))

    if request.method == 'POST':
        consent = request.form.get('otp_consent')
        if not consent:
            flash('You must consent to receive an OTP.', 'warning')
            return redirect(url_for('auth.login'))
            
        identifier = request.form.get('identifier', '').strip()
        
        user = User.query.filter((User.phone_number == identifier) | (User.email == identifier)).first()
        if user:
            # Store user ID in session temporarily
            session['pending_user_id'] = user.id
            session['auth_method'] = identifier
            session['auth_action'] = 'login'
            
            otp = str(random.randint(100000, 999999))
            session['otp'] = otp
            threading.Thread(target=send_otp_helper, args=(identifier, otp)).start()
            flash(f"An OTP has been sent to {identifier}.", "info")
                
            return redirect(url_for('auth.verify_otp'))
            
        flash('No account found with that phone number or email.', 'danger')

    return render_template('auth/login.html')

@auth_bp.route('/verify_otp', methods=['GET', 'POST'])
def verify_otp():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.home'))
        
    if 'auth_action' not in session or 'auth_method' not in session:
        flash("Session expired. Please start over.", "warning")
        return redirect(url_for('auth.login'))
        
    if request.method == 'POST':
        entered_otp = request.form.get('otp')
        identifier = session.get('auth_method')
        
        is_valid = False
        
        # Verify locally generated OTP
        if entered_otp and session.get('otp') and entered_otp.strip() == session.get('otp'):
            is_valid = True

        if is_valid:
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
                    pin_hash=hashed_pin,
                    otp_consent=reg_data.get('otp_consent', False)
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
    flash(f"A new OTP has been sent to {identifier}.", "info")
        
    return redirect(url_for('auth.verify_otp'))

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.home'))

    if request.method == 'POST':
        consent = request.form.get('otp_consent')
        if not consent:
            flash('You must consent to receive OTPs and notifications.', 'warning')
            return redirect(url_for('auth.register'))

        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        phone = request.form.get('phone_number', '').strip()
        otp_method = request.form.get('otp_method')

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
        session['auth_action'] = 'register'
        
        # Decide where to send OTP based on selected method
        if otp_method == 'email' and email:
            identifier = email
        elif otp_method == 'sms' and phone:
            identifier = phone
        else:
            identifier = email if email else phone

        session['auth_method'] = identifier
        session['reg_data'] = {
            'name': name,
            'email': email,
            'phone': phone,
            'otp_consent': True if consent else False
        }
        
        otp = str(random.randint(100000, 999999))
        session['otp'] = otp
        threading.Thread(target=send_otp_helper, args=(identifier, otp)).start()
        flash(f"An OTP has been sent to {identifier} to complete registration.", "info")
            
        return redirect(url_for('auth.verify_otp'))

    return render_template('auth/register.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth_bp.route('/setup-otp', methods=['GET'])
def setup_otp():
    import os
    return render_template('setup_otp.html',
                           email_user=os.environ.get('EMAIL_USER', ''),
                           email_pass=os.environ.get('EMAIL_PASS', ''),
                           twilio_sid=os.environ.get('TWILIO_ACCOUNT_SID', ''),
                           twilio_token=os.environ.get('TWILIO_AUTH_TOKEN', ''),
                           twilio_phone=os.environ.get('TWILIO_PHONE_NUMBER', ''))

def update_env_file(key, value):
    import os
    env_path = os.path.join(os.path.dirname(__file__), '.env')
    
    lines = []
    if os.path.exists(env_path):
        with open(env_path, 'r') as f:
            lines = f.readlines()
            
    updated = False
    for i, line in enumerate(lines):
        if line.startswith(f"{key}="):
            lines[i] = f"{key}={value}\n"
            updated = True
            break
            
    if not updated:
        lines.append(f"{key}={value}\n")
        
    with open(env_path, 'w') as f:
        f.writelines(lines)
        
    os.environ[key] = value

@auth_bp.route('/setup-otp/save', methods=['POST'])
def setup_otp_save():
    setup_type = request.form.get('type')
    
    if setup_type == 'email':
        email_user = request.form.get('email_user')
        email_pass = request.form.get('email_pass')
        
        update_env_file('EMAIL_USER', email_user)
        update_env_file('EMAIL_PASS', email_pass)
        
        # Test Email directly
        import smtplib
        from email.mime.text import MIMEText
        from email.mime.multipart import MIMEMultipart
        
        try:
            msg = MIMEMultipart()
            msg['From'] = email_user
            msg['To'] = email_user # Send to self for test
            msg['Subject'] = "CashX Test OTP"
            msg.attach(MIMEText("This is a test OTP from your CashX Setup.", 'plain'))
            
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(email_user, email_pass)
            server.send_message(msg)
            server.quit()
            flash("SUCCESS! Email test sent. Check your inbox.", "success")
        except Exception as e:
            flash(f"ERROR: Could not connect to Gmail. Details: {str(e)}", "danger")
            
    elif setup_type == 'sms':
        twilio_sid = request.form.get('twilio_sid')
        twilio_token = request.form.get('twilio_token')
        twilio_phone = request.form.get('twilio_phone')
        test_phone = request.form.get('test_phone')
        
        update_env_file('TWILIO_ACCOUNT_SID', twilio_sid)
        update_env_file('TWILIO_AUTH_TOKEN', twilio_token)
        update_env_file('TWILIO_PHONE_NUMBER', twilio_phone)
        
        # Test SMS
        try:
            from twilio.rest import Client
            client = Client(twilio_sid, twilio_token)
            message = client.messages.create(
                body="This is a test OTP from CashX Setup.",
                from_=twilio_phone,
                to=test_phone
            )
            flash(f"SUCCESS! SMS test sent. SID: {message.sid}", "success")
        except Exception as e:
            flash(f"ERROR: Could not send Twilio SMS. Details: {str(e)}", "danger")
            
    return redirect(url_for('auth.setup_otp'))
