from flask import Blueprint, render_template, redirect, url_for, request
from . import db
from .models import User, Event
from flask_login import current_user, login_required

bp = Blueprint('main', __name__)

@bp.route('/', methods=['GET', 'POST'])
def index():
    events = Event.query.order_by(Event.date_created).all()
    users = User.query.order_by(User.id).all()
    return render_template('index.html', events=events, user=current_user, include_header=True)


