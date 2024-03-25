import os
from flask import Blueprint, jsonify, request,render_template,redirect,url_for,flash
from admin.order.models import *
from admin.address.models import *
from admin.payment.models import *
from admin.feedback.models import *
from config import UPLOADS_DIR
from initialize import db
from flask_login import current_user

blueprint = Blueprint('ordering', __name__)


@blueprint.route('/cart', methods=["GET","POST"])
def cart():
    context = {}
    order = None # for check if exist a cart
    for item in current_user.orders:
        if item.status == "cart":
            order = item
    context['order'] = order

    if request.method == "GET":
        return render_template('ordering/cart.html',**context)
    
    elif request.method == 'POST':
        for item in order.orderitems:
            item.quantity = request.form.get(str(item.id)) # gets new quantity from cart
            db.session.commit()
        return redirect(url_for('ordering.checkout',id=order.id))



@blueprint.route('/add_item/<int:id>', methods=["GET","POST"])
def add_item(id):
    quantity = int(request.args.get('quantity'))

    order = None # for check if exist a cart
    for item in current_user.orders:
        if item.status == "cart":
            order = item

    if not order: # create a cart order if not exist
        order = Order(user_id=current_user.id)
        db.session.add(order)
        db.session.commit()

    order_item = None # check for dublicates orderItems
    for item in order.orderitems:
        if item.product.id == id:
            order_item = item

    if not order_item: # create order item if not exist
        order_item = OrderItem(order_id=order.id,product_id=id,quantity=quantity)
        db.session.add(order_item)
        db.session.commit()
    else:
        order_item.quantity += quantity # add quantity if exist
        db.session.commit()
    
    return redirect(url_for('site.product',id=id))



@blueprint.route('/delete_item/<int:id>')
def delete_item(id):
    oi = OrderItem.query.get_or_404(id)
    db.session.delete(oi)
    db.session.commit()
    return redirect(url_for('ordering.cart'))



@blueprint.route('/checkout/<int:id>', methods=["GET","POST"])
def checkout(id):
    order = Order.query.get_or_404(id)
    context = {}
    context['order'] = order

    if request.method == "GET":
        return render_template('ordering/checkout.html',**context)
    
    elif request.method == 'POST':
        country = request.form.get('country')
        city = request.form.get('city')
        street = request.form.get('street')
        postal_code = request.form.get('postal_code')
        method = request.form.get('method')
        a = Address(order_id=order.id,country=country,city=city,
                        street=street,postal_code=postal_code)
        p = Payment(order_id=order.id,method=method,amount=order.total_amount)        
        order.status = 'sending'
        db.session.add(a)
        db.session.add(p)
        db.session.commit()
        flash("Order Placed !", 'info')
        return redirect (url_for('dahsbord.profile'))
    


@blueprint.route('/dashboard', methods=["GET","POST"])
def dashboard():
    context = {}
    context['orders'] = Order.query.all()
    if request.method=="GET":
        return render_template('ordering/dashboard.html',**context)
    
    if request.method=="POST":
        username = request.form.get('username',"").strip()
        password = request.form.get('password',"").strip()
        email = request.form.get('email',"").strip()

        current_user.username = username
        current_user.email = email
        if password:
            current_user.password = password
        db.session.commit()
        return render_template('ordering/dashboard.html',**context)



@blueprint.route('/add_feedback/<int:id>', methods=["GET","POST"])
def add_feedback(id):
    if request.method == "GET":
        return render_template('ordering/feedback.html')
    
    if request.method == 'POST':
        rating = int(request.form.get('rating',""))
        comment = request.form.get('comment','').strip()

        order = Order.query.get_or_404(id)
        if order.feedbacks:
            flash('Feedback already registered', 'danger')
            return redirect(url_for('ordering.dashboard'))
        
        f = FeedBack(user_id=current_user.id,order_id=order.id,rating=rating,comment=comment)
        db.session.add(f)
        db.session.commit()
        flash('Feedback successfuly registered !')
        return redirect(url_for('ordering.dashboard'))