from initialize import db
from datetime import datetime

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False,unique=True)
    description = db.Column(db.Text, nullable=True)
    image = db.Column(db.String(80), nullable=True)
    create_at = db.Column(db.DateTime, default=datetime.now)
    products = db.relationship("Product", backref="category", cascade='all, delete-orphan', lazy=True)

    def __repr__(self):
        return '<Category %r>' % self.name
