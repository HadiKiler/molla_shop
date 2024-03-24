from flask import Blueprint, jsonify, request,render_template,redirect,url_for
from admin.order.models import *
from initialize import db
from flask_login import current_user


blueprint = Blueprint('dashbord', __name__)


@blueprint.route('/cart', methods=["GET","POST"])
def cart():
    context = {}
    order = None # for check if exist a cart
    for item in current_user.orders:
        if item.status == "cart":
            order = item
    context['order'] = order
    if request.method == "GET":
        return render_template('dashbord/cart.html',**context)
    
    elif request.method == 'POST':
        for item in order.orderitems:
            item.quantity = request.form.get(str(item.id)) # gets new quantity from cart
            db.session.commit()
        return redirect(url_for('dashbord.checkout'))


@blueprint.route('/checkout', methods=["GET","POST"])
def checkout():
    return render_template('dashbord/checkout.html')


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
    return redirect(url_for('dashbord.cart'))