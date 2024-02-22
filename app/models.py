from . import db
from flask_login import UserMixin
from datetime import datetime

event_attendance = db.Table('event_attendance',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('event_id', db.Integer, db.ForeignKey('event.id'), primary_key=True)
)

class User(db.Model, UserMixin):
    # User credentials
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)

    # User details
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    bio = db.Column(db.String(400), nullable=True)
    date_joined = db.Column(db.DateTime, default=datetime.utcnow)  
    profile_pic = db.Column(db.String(200), nullable=False, default='default.jpg')

    # User relationships
    events_attending = db.relationship('Event', secondary=event_attendance,
    backref=db.backref('attendees', lazy='dynamic'))


    def full_name(self):
        return self.first_name + ' ' + self.last_name

    def __repr__(self):
        return '<User %r>' % self.username

class Event(db.Model):
    # Event details
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    club = db.Column(db.String(200), nullable=True)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    location = db.Column(db.String(200), nullable=True)
    dateTime = db.Column(db.String(200), nullable=True)

    # Foreign keys
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    club_id = db.Column(db.Integer, db.ForeignKey('club.id'))

    # Event Relationships
    user = db.relationship('User', backref=db.backref('events', lazy=True))
    club_association = db.relationship('Club', backref=db.backref('events', lazy=True))

    def __repr__(self):
        return '<Event %r>' % self.id

class Club(db.Model):
    # Club details
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    location = db.Column(db.String(200), nullable=True)

    # Foreign keys
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    # Club Relationships
    user = db.relationship('User', backref=db.backref('clubs', lazy=True))

    def __repr__(self):
        return '<Club %r>' % self.id