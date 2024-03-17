from initialize import db
from datetime import datetime

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.Text , nullable=True)
    price = db.Column(db.Float, nullable=False)
    category_id = db.Column(db.Integer,
        db.ForeignKey('category.id'), nullable=False)
    orderitems = db.relationship("OrderItem", backref="product", lazy=True)

    def __repr__(self):
        return '<Product %r>' % self.name
