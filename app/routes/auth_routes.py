from flask import Blueprint, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import User
from app import db

# Create the Blueprint for authentication
auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/auth/register', methods=['POST'])
def register_user():
    email = request.form.get('email')
    password = request.form.get('password')

    # 1. Check if the user already exists
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return redirect(url_for('pages.login')) # Send them to login if they exist

    # 2. Securely hash the password (military-grade PBKDF2)
    hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

    # 3. Create the user and save to the database
    new_user = User(email=email, password_hash=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    # 4. Log them in (save ID to session cookie) and send to Command Center
    session['user_id'] = new_user.id
    return redirect(url_for('pages.dashboard'))

@auth_bp.route('/auth/login', methods=['POST'])
def login_user():
    email = request.form.get('email')
    password = request.form.get('password')

    # 1. Find the user
    user = User.query.filter_by(email=email).first()

    # 2. Verify the password hash matches
    if user and check_password_hash(user.password_hash, password):
        session['user_id'] = user.id
        return redirect(url_for('pages.dashboard'))
    
    # If they fail, kick them back to the login page
    return redirect(url_for('pages.login'))

@auth_bp.route('/auth/logout')
def logout():
    # Destroy the session
    session.pop('user_id', None)
    return redirect(url_for('pages.index'))
