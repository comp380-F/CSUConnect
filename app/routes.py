from flask import Blueprint, render_template, redirect, url_for, request
from . import db
from .models import User, Post
from flask_login import current_user, login_required

bp = Blueprint('main', __name__)

@bp.route('/', methods=['GET', 'POST'])
def index():
    posts = Post.query.order_by(Post.date_created).all()
    users = User.query.order_by(User.id).all()
    return render_template('index.html', posts=posts, user=current_user)


