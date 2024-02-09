from flask import Blueprint, render_template, redirect, url_for, flash, request
from . import db
from .models import User, Post
from flask_login import login_manager, login_user, current_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash

bp = Blueprint('main', __name__)

@bp.route('/', methods=['GET', 'POST'])
def index():
    posts = Post.query.order_by(Post.date_created).all()
    users = User.query.order_by(User.id).all()
    return render_template('index.html', posts=posts, user=current_user)

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        hashed_password = generate_password_hash(password)
        new_user = User(username=username, password_hash=hashed_password)

        try:
            db.session.add(new_user)
            db.session.commit()
            return redirect('/')
        except:
            return 'Failed to register user'
        
    return render_template('register.html', user=current_user)

@bp.route('/login', methods=['GET', 'POST'])
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
    
    return render_template('login.html', user=current_user)

@bp.route('/logout')
def logout():
    logout_user()
    return redirect('/')

# Routes

@bp.route('/new-post', methods=['POST', 'GET'])
@login_required
def new_post():
    if request.method == 'POST':
        if not current_user.is_authenticated:
            return redirect('/login')
        
        post_title = request.form['title']
        post_content = request.form['content']

        new_post = Post(title=post_title, content=post_content, user_id=current_user.id)

        try:
            db.session.add(new_post)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your post'
    else:
        posts = Post.query.order_by(Post.date_created).all()

        return render_template("new-post.html", posts=posts)


@bp.route('/delete/<int:id>')
def delete(id):
    post_to_delete = Post.query.get_or_404(id)

    try:
        db.session.delete(post_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting that post'


@bp.route('/update/<int:id>', methods=['GET', 'POST'])
@login_required
def update(id):
    post = Post.query.get_or_404(id)

    if request.method == 'POST':
        post.content = request.form['content']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue updating your post'
    else:
        return render_template('update.html', post=post)