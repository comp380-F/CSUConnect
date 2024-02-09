from flask import Blueprint, render_template, redirect
from .models import User, Post
from flask_login import current_user

user_bp = Blueprint('user', __name__)

@user_bp.route('/profile', methods=['GET', 'POST'])
def profile():
    if current_user.is_authenticated:
        return render_template('profile.html', user=current_user, include_header=True)
    else:
        return redirect('/')
