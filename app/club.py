from flask import Blueprint, render_template, redirect
from flask_login import current_user
from .models import Club

club_bp = Blueprint('club', __name__)

@club_bp.route('/club/<int:id>', methods=['GET', 'POST'])
def club(id):
    club = Club.query.get_or_404(id)
    return render_template('club.html', user=current_user, club=club, include_header=True)


@club_bp.route('/clubs', methods=['GET', 'POST'])
def all_clubs():
    clubs = Club.query.all()
    return render_template('all_clubs.html', user=current_user, clubs=clubs, include_header=True)