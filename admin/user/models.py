from initialize import db
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), nullable=True)
    is_admin = db.Column(db.Boolean, default = False)
    register_date = db.Column(db.DateTime, default=datetime.now)
    adresses = db.relationship("Adress", backref="user",cascade='all, delete-orphan', lazy=True)
    orders = db.relationship("Order", backref="user",cascade='all, delete-orphan', lazy=True)
    feedbacks = db.relationship("FeedBack",cascade='all, delete-orphan', backref="user", lazy=True)
    logs = db.relationship("Log", backref="user",cascade='all, delete-orphan', lazy=True)
    
    
    def __repr__(self):
        return '<User %r>' % self.username
