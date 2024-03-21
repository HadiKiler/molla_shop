
from flask import Blueprint, jsonify, request
from .models import Address
from initialize import db
from admin.log.models import save_log

blueprint = Blueprint('address', __name__)


@blueprint.route('/address', methods=["GET"])
def addresses():
    qs = Address.query.all()
    data = []
    for item in qs:
        data.append({
            "id": item.id,
            'order_id': item.order_id,
            'country': item.country,
            'city': item.city,
            'address': item.address,
            'postal_code': item.postal_code
        })
    response = jsonify(data)
    response.headers['Access-Control-Expose-Headers'] = 'Content-Range'
    response.headers['Content-Range'] = len(data)
    return response


@blueprint.route('/address/<int:id>', methods=["GET"])
def read_address(id):
    a = Address.query.get(id)
    return jsonify({
            "id": a.id,
            'order_id': a.order_id,
            'country': a.country,
            'city': a.city,
            'address': a.address,
            'postal_code': a.postal_code
        })


@blueprint.route('/address/<int:id>', methods=["PUT"])
def update_address(id):
    order_id = request.json.get('order_id', "")
    country = request.json.get('country', "").strip()
    city = request.json.get('city', "").strip()
    address = request.json.get('address', "").strip()
    postal_code = request.json.get('postal_code', "").strip()

    a = Address.query.get(id)
    a.order_id = order_id
    a.country = country
    a.city = city
    a.address = address
    a.postal_code = postal_code
    db.session.commit()
    save_log(request,f"address {id} updated !")
    return jsonify({
            "id": a.id,
            'order_id': a.order_id,
            'country': a.country,
            'city': a.city,
            'address': a.address,
            'postal_code': a.postal_code
        })


@blueprint.route('/address/<int:id>', methods=["DELETE"])
def delete_address(id):
    a = Address.query.get(id)
    db.session.delete(a)
    db.session.commit()
    save_log(request,f"address {id} deleted !")
    return jsonify({
            "id": a.id,
            'order_id': a.order_id,
            'country': a.country,
            'city': a.city,
            'address': a.address,
            'postal_code': a.postal_code
        })
