from initialize import db
from datetime import datetime


# status of orders
# cart
# sending
# Completed

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer,
            db.ForeignKey('user.id'), nullable=False)
    order_date = db.Column(db.DateTime, default=datetime.now)
    status = db.Column(db.String(20), default="cart", nullable=False)
    orderitems = db.relationship("OrderItem", backref="order", cascade='all, delete-orphan', lazy=True)
    payments = db.relationship("Payment", backref="order",cascade='all, delete-orphan', lazy=True)
    feedbacks = db.relationship("FeedBack", backref="order",cascade='all, delete-orphan', lazy=True)
    adresses = db.relationship("Address", backref="order",cascade='all, delete-orphan', lazy=True)
   
    @property
    def total_amount(self):
        total = 0
        for orderitem in self.orderitems: # calculate total amount of order items
           total+=(orderitem.product.price * orderitem.quantity)
        return total
    
    def __repr__(self):
        return '<Order %r>' % self.id
    
    

class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer,
            db.ForeignKey('order.id'), nullable=False)
    product_id = db.Column(db.Integer,
            db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable = False)

    def __repr__(self):
        return '<OrderItem %r>' % self.id
