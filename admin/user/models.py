from initialize import db,login_manager
from datetime import datetime
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), nullable=True)
    is_admin = db.Column(db.Boolean, default = False)
    image = db.Column(db.String(80), default='default.png')
    register_date = db.Column(db.DateTime, default=datetime.now)
    orders = db.relationship("Order", backref="user",cascade='all, delete-orphan', lazy=True)
    feedbacks = db.relationship("FeedBack",cascade='all, delete-orphan', backref="user", lazy=True)
    logs = db.relationship("Log", backref="user",cascade='all, delete-orphan', lazy=True)
    
    
    def __repr__(self):
        return '<User %r>' % self.username
