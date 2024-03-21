from initialize import db
from datetime import datetime


class Log(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer,
            db.ForeignKey('user.id'), nullable=False)
    action = db.Column(db.String(80), nullable=False)
    action_date = db.Column(db.DateTime, default=datetime.now)


    def __repr__(self):
        return '<Payment %r>' % self.id

def save_log(request, message):
    print(request.headers)
    user_id = request.headers.get("User")
    l = Log(user_id=user_id,action=message)
    db.session.add(l)
    db.session.commit()