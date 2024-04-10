from initialize import db
from datetime import datetime


class Log(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer,
            db.ForeignKey('user.id'), nullable=False)
    user_ip = db.Column(db.String(80), nullable=True)
    action = db.Column(db.String(80), nullable=False)
    action_date = db.Column(db.DateTime, default=datetime.now)


    def __repr__(self):
        return '<Payment %r>' % self.id

def save_log(request, message):
    user_id = request.headers.get("User")
    user_ip = request.remote_addr
    l = Log(user_id=user_id, action=message, user_ip=user_ip)
    db.session.add(l)
    db.session.commit()