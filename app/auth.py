from flask import Blueprint, render_template, redirect, url_for, flash, request
from . import db
from .models import User, Event
from flask_login import login_manager, login_user, current_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash


auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        first_name = request.form['firstname']
        last_name = request.form['lastname']

        hashed_password = generate_password_hash(password)
        new_user = User(username=username, 
                        password_hash=hashed_password, 
                        email=email, 
                        first_name=first_name,
                        last_name=last_name)

        try:
            db.session.add(new_user)
            db.session.commit()
            return redirect('/')
        except:
            return 'Failed to register user'
        
    return render_template('register.html', user=current_user, include_header=True)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            return redirect('/')
        else:
            flash('Login failed. Check your username and password.')
    
    return render_template('login.html', user=current_user, include_header=True)

@auth_bp.route('/logout')
def logout():
    logout_user()
    return redirect('/')