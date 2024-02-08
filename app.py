from flask import Flask, render_template, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager, login_user, current_user, logout_user, login_required
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'my_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login' # Where to redirect when login is required

# Class models

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    user = db.relationship('User', backref=db.backref('posts', lazy=True))

    def __repr__(self):
        return '<Post %r>' % self.id


# Login Routes
    
@login_manager.user_loader
def load_user(user_id):
    return db.session.get((User), int(user_id))

@app.route('/register', methods=['GET', 'POST'])
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
        
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
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
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect('/')

# Routes
    
@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        if not current_user.is_authenticated:
            return redirect('/login')
        
        post_content = request.form['content']
        new_post = Post(content=post_content, user_id=current_user.id)

        try:
            db.session.add(new_post)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your post'
    else:
        posts = Post.query.order_by(Post.date_created).all()

        return render_template("index.html", posts=posts)


@app.route('/delete/<int:id>')
def delete(id):
    post_to_delete = Post.query.get_or_404(id)

    try:
        db.session.delete(post_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting that post'


@app.route('/update/<int:id>', methods=['GET', 'POST'])
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

# Main
    
if __name__ == "__main__":
    app.run(debug=True)
