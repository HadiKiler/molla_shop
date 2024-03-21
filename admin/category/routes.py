from flask import Blueprint, jsonify,request
from initialize import db
from .models import Category
from admin.log.models import save_log


blueprint = Blueprint('category', __name__)


@blueprint.route('/category', methods=["GET"])
def categories():
    qs = Category.query.all()
    data = []
    for item in qs:
        data.append({
            "id": item.id,
            'name': item.name,
            'create_at': item.create_at
        })
    response = jsonify(data)
    response.headers['Access-Control-Expose-Headers'] = 'Content-Range'
    response.headers['Content-Range'] = len(data)
    return response


@blueprint.route('/category/<int:id>', methods=["GET"])
def read_category(id):
    c = Category.query.get(id)
    return jsonify({
            "id": c.id,
            'name': c.name,
            'description': c.description,
            'create_at': c.create_at
        })


@blueprint.route('/category', methods=["POST"])
def create_category():
    name = request.json.get('name', "").strip()
    description = request.json.get('description', "").strip()

    c = Category.query.filter_by(name=name).first()
    if c:
        name = name + " Copy"

    c = Category(name=name, description=description)
    db.session.add(c)
    db.session.commit()
    save_log(request,f"category {c.id} created !")
    return jsonify({
            "id": c.id,
            'name': c.name,
            'description': c.description,
            'create_at': c.create_at
        })


@blueprint.route('/category/<int:id>', methods=["PUT"])
def update_category(id):
    name = request.json.get('name', "").strip()
    description = request.json.get('description', "").strip()
    categories = []
    for category in Category.query.all(): 
        if category.id != id:
            categories.append(category)

    c = None
    for category in categories:
        if category.name == name: 
            c = category
            break
    if c:
        name = name + " Copy"
    c = Category.query.get(id)
    c.name = name
    c.description = description 
    db.session.commit()
    save_log(request,f"category {id} updated !")
    return jsonify({
            "id": c.id,
            'name': c.name,
            'description': c.description,
            'create_at': c.create_at
        })



@blueprint.route('/category/<int:id>', methods=["DELETE"])
def delete_category(id):
    c = Category.query.get(id)
    db.session.delete(c)
    db.session.commit()
    save_log(request,f"category {id} deleted !")
    return jsonify({
            "id": c.id,
            'name': c.name,
            'description': c.description,
            'create_at': c.create_at
        })
