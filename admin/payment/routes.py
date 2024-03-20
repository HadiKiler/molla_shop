from flask import Blueprint, jsonify, request
from .models import Payment
from initialize import db
from ast import literal_eval

blueprint = Blueprint('payment', __name__)


@blueprint.route('/payment', methods=["GET"])
def payments():
    filter = literal_eval(request.args.get('filter')) # change strig to dict
    qs = []
    try:
        q = filter['q']
        for payment in Payment.query.all():
            if str(payment.order_id) == q or payment.method == q:
                qs.append(payment)
    except:
        qs = Payment.query.all()
    data = []
    for payment in qs:
        data.append({
            "id": payment.id,
            'order_id': payment.order_id,
            'method': payment.method,
            'amount': payment.amount,
            'payment_date': payment.payment_date,
        })
    response = jsonify(data)
    response.headers['Access-Control-Expose-Headers'] = 'Content-Range'
    response.headers['Content-Range'] = len(data)
    return response


@blueprint.route('/payment/<int:id>', methods=["GET"])
def read_payment(id):
    p = Payment.query.get(id)
    return jsonify({
            "id": p.id,
            'order_id': p.order_id,
            'method': p.method,
            'amount': p.amount,
            'payment_date': p.payment_date,
        })
