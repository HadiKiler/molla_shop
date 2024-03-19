from flask import Blueprint, jsonify
from .models import Category


blueprint = Blueprint('category', __name__)


@blueprint.route('/category', methods=["GET"])
def categories():
    qs = Category.query.all()
    data = []
    for item in qs:
        data.append({
            "id": item.id,
            'name': item.name,
            'description': item.description,
            'create_at': item.create_at,
        })
    response = jsonify(data)
    response.headers['Access-Control-Expose-Headers'] = 'Content-Range'
    response.headers['Content-Range'] = len(data)
    return response