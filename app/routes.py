from flask import Blueprint, render_template, redirect, url_for, request
from . import db
from .models import User, Event, Post
from flask_login import current_user, login_required

bp = Blueprint('main', __name__)

@bp.route('/', methods=['GET', 'POST'])
def index():
    events = Event.query.order_by(Event.date_created.desc()).all()
    posts = Post.query.order_by(Post.date_created.desc()).all()
    return render_template('index.html', posts=posts, events=events, user=current_user, include_header=True)


