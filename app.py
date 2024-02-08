from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
db = SQLAlchemy(app)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Post %r>' % self.id

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        post_content = request.form['content']
        new_post = Post(content=post_content)

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


if __name__ == "__main__":
    app.run(debug=True)
