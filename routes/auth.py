from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from models.models import db, User
from utils.authentication import bcrypt, log_activity, get_real_ip
from datetime import datetime

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))
    return render_template('index.html')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        user     = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password_hash, password):
            if not user.is_active:
                flash('Your account has been disabled. Contact admin.', 'danger')
                return render_template('login.html')
            login_user(user, remember=True)
            user.last_login = datetime.utcnow()
            db.session.commit()
            real_ip = get_real_ip()
            log_activity(user.id, 'LOGIN', f'User logged in from {real_ip}', ip=real_ip)
            return redirect(url_for('dashboard.index'))
        flash('Invalid username or password.', 'danger')
        log_activity(user.id if user else 0, 'LOGIN', f'Failed login for {username}',
                     ip=get_real_ip(), status='FAILED')
    return render_template('login.html')


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email    = request.form.get('email',    '').strip().lower()
        password = request.form.get('password', '')
        company  = request.form.get('company',  '').strip()

        if User.query.filter_by(username=username).first():
            flash('Username already taken.', 'danger')
        elif User.query.filter_by(email=email).first():
            flash('Email already registered.', 'danger')
        elif len(password) < 8:
            flash('Password must be at least 8 characters.', 'warning')
        else:
            user = User(
                username      = username,
                email         = email,
                password_hash = bcrypt.generate_password_hash(password).decode('utf-8'),
                company       = company or 'Independent',
                role          = 'user',
            )
            db.session.add(user)
            db.session.commit()
            login_user(user)
            log_activity(user.id, 'REGISTER', f'New user registered: {username}', ip=get_real_ip())
            flash('Account created! Welcome to QuantumVault.', 'success')
            return redirect(url_for('dashboard.index'))
    return render_template('register.html')


@auth_bp.route('/logout')
@login_required
def logout():
    log_activity(current_user.id, 'LOGOUT', ip=get_real_ip())
    logout_user()
    flash('You have been securely logged out.', 'info')
    return redirect(url_for('auth.login'))
