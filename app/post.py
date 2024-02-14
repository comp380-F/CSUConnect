from flask import Blueprint, render_template, redirect, url_for, request
from . import db
from .models import User, Post
from flask_login import current_user, login_required

post_bp = Blueprint('post', __name__)

@post_bp.route('/new-post', methods=['POST', 'GET'])
@login_required
def new_post():
    if request.method == 'POST':
        if not current_user.is_authenticated:
            return redirect('/login')

        post_title = request.form['title']
        post_description = request.form['description']
        post_club = request.form['club']

        new_post = Post(title=post_title, description=post_description, club=post_club, user_id=current_user.id)

        try:
            db.session.add(new_post)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your post'
    else:
        posts = Post.query.order_by(Post.date_created).all()

        return render_template("new-post.html", posts=posts, user=current_user, include_header=True)


@post_bp.route('/delete/<int:id>')
def delete(id):
    post_to_delete = Post.query.get_or_404(id)

    try:
        db.session.delete(post_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting that post'


@post_bp.route('/update/<int:id>', methods=['GET', 'POST'])
@login_required
def update(id):
    post = Post.query.get_or_404(id)

    if request.method == 'POST':
        post.description = request.form['description']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue updating your post'
    else:
        return render_template('update.html', post=post, include_header=True)
