from flask import Blueprint, redirect, url_for, render_template, request, jsonify
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from models import User
from app import db, oauth

auth_bp = Blueprint('auth', __name__)

google = oauth.register(
    name='google',
    client_id='GOOGLE_CLIENT_ID',
    client_secret='GOOGLE_CLIENT_SECRET',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None,
    access_token_url='https://accounts.google.com/o/oauth2/token',
    access_token_params=None,
    refresh_token_url=None,
    redirect_uri='http://127.0.0.1:5000/auth/google/callback',
    client_kwargs={'scope': 'openid email profile'},
)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    # if request.method == 'POST':
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    # Ищем пользователя по email
    user = User.query.filter_by(email=email).first()

    if user and check_password_hash(user.password, password):
        # Если пароль верен, логиним пользователя
        login_user(user)
        return jsonify({"message": "Login successful"}), 200
    else:
        return jsonify({"message": "Invalid email or password"}), 401

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        hashed_password = generate_password_hash(password, method='sha256')
        new_user = User(email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for('main.home'))
    return render_template('register.html')

@auth_bp.route('/login/google')
def login_google():
    return google.authorize_redirect(url_for('auth.google_callback', _external=True))

@auth_bp.route('/auth/google/callback')
def google_callback():
    token = google.authorize_access_token()
    resp = google.get('userinfo')
    user_info = resp.json()
    user = User.query.filter_by(email=user_info['email']).first()
    if not user:
        user = User(email=user_info['email'], google_id=user_info['sub'])
        db.session.add(user)
        db.session.commit()
    login_user(user)
    return redirect(url_for('main.home'))

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
