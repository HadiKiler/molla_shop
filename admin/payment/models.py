from initialize import db
from datetime import datetime


class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer,
            db.ForeignKey('order.id'), nullable=False)
    method = db.Column(db.String(20), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    payment_date = db.Column(db.DateTime, default=datetime.now)


    def __repr__(self):
        return '<Payment %r>' % self.id
