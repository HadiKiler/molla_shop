from initialize import db

class Address(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer,
            db.ForeignKey('order.id'), nullable=False) 
    country = db.Column(db.String(20), nullable=False)
    city = db.Column(db.String(20), nullable=False)
    street = db.Column(db.Text, nullable=False)
    postal_code = db.Column(db.String(10), nullable=False)

    def __repr__(self):
        return '<Adress %r>' % self.id
