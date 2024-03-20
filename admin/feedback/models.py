from initialize import db
from datetime import datetime

class FeedBack(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer,
            db.ForeignKey('user.id'), nullable=False)
    order_id = db.Column(db.Integer,
        db.ForeignKey('order.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text, nullable=True)
    feedback_date = db.Column(db.DateTime, default=datetime.now)

    def __repr__(self):
        return '<FeedBack %r>' % self.id
