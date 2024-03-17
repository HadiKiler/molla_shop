from initialize import db

class Adress(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer,
            db.ForeignKey('user.id'), nullable=False) 
    country = db.Column(db.String(20), nullable=False)
    city = db.Column(db.String(20), nullable=False)
    address = db.Column(db.Text, nullable=False)
    postal_code = db.Column(db.String(10), nullable=False)

    def __repr__(self):
        return '<Adress %r>' % self.id
