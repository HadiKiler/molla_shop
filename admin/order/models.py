from initialize import db
from datetime import datetime


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer,
            db.ForeignKey('user.id'), nullable=False)
    order_date = db.Column(db.DateTime, default=datetime.now)
    total_amount = db.Column(db.Float, nullable=True)
    status = db.Column(db.String(20), nullable=False)
    orderitems = db.relationship("OrderItem", backref="order", lazy=True)
    payments = db.relationship("Payment", backref="order", lazy=True)
    feedbacks = db.relationship("FeedBack", backref="order", lazy=True)

    def __repr__(self):
        return '<Order %r>' % self.id


class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer,
            db.ForeignKey('order.id'), nullable=False)
    product_id = db.Column(db.Integer,
            db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable = False)
    unit_price = db.Column(db.Float, nullable = False)

    def __repr__(self):
        return '<OrderItem %r>' % self.id
