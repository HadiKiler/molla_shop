from flask import Blueprint, jsonify, request
from .models import Order
from initialize import db


blueprint = Blueprint('order', __name__)


@blueprint.route('/order', methods=["GET"])
def orders():
    qs = Order.query.all()
    data = []
    for order in qs:
        data.append({
            "id": order.id,
            'user_id': order.user_id,
            'order_date': order.order_date,
            'total_amount': order.total_amount,
            'status': order.status,
        })
    response = jsonify(data)
    response.headers['Access-Control-Expose-Headers'] = 'Content-Range'
    response.headers['Content-Range'] = len(data)
    return response


@blueprint.route('/order/<int:id>', methods=["GET"])
def read_order(id):
    o = Order.query.get(id)

    items = {}
    for orderitem in o.orderitems:
        items[orderitem.product.name] = orderitem.quantity
    
    return jsonify({
            "id": o.id,
            'user_id': o.user_id,
            'order_date': o.order_date,
            'total_amount': o.total_amount,
            'status': o.status,
            'items': items
        })



@blueprint.route('/order/<int:id>', methods=["PUT"])
def update_order(id):
    o = Order.query.get(id)
    user_id = int(request.json.get('user_id', ""))
    status = request.json.get('status', "").strip()

    o.user_id = user_id
    o.status = status
    db.session.commit()

    return jsonify({
            "id": o.id,
            'user_id': o.user_id,
            'order_date': o.order_date,
            'total_amount': o.total_amount,
            'status': o.status,
        })


@blueprint.route('/order/<int:id>', methods=["DELETE"])
def delete_order(id):
    o = Order.query.get(id)
    db.session.delete(o)
    db.session.commit()

    return jsonify({
            "id": o.id,
            'user_id': o.user_id,
            'order_date': o.order_date,
            'status': o.status,
    })


