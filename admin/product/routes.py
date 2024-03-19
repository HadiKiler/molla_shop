import os
from flask import send_from_directory, url_for
from flask import Blueprint, jsonify, request
from .models import Product
from initialize import db
from config import UPLOADS_DIR, HOST


blueprint = Blueprint('product', __name__)


@blueprint.route('/uploads/<filename>')
def uploads(filename=''):
    return send_from_directory(UPLOADS_DIR, filename)

@blueprint.route('/product', methods=["GET"])
def products():
    qs = Product.query.all()
    data = []
    for item in qs:
        data.append({
            "id": item.id,
            'category_id': item.category_id,
            'name': item.name,
            'description': item.description,
            'price': item.price,
            'image': HOST + url_for('product.uploads',filename=item.image)
        })
    response = jsonify(data)
    response.headers['Access-Control-Expose-Headers'] = 'Content-Range'
    response.headers['Content-Range'] = len(data)
    return response


@blueprint.route('/product/<int:id>', methods=["GET"])
def read_product(id):
    p = Product.query.get(id)
    return jsonify({
            "id": p.id,
            'category_id': p.category_id,
            'name': p.name,
            'description': p.description,
            'price': p.price,
            'image': HOST + url_for('product.uploads',filename=p.image)
        })

@blueprint.route('/product', methods=["POST"])
def create_product():
    category_id = int(request.form.get('category_id', "").strip())
    name = request.form.get('name', "").strip()
    description = request.form.get('description', "").strip()
    price = request.form.get('price', "").strip()
    image = request.files.get("image","")

    p = Product(category_id=category_id, name=name,
                 description=description, price=price,
                 image=image.filename)
    image.save(os.path.join(UPLOADS_DIR, image.filename))
    db.session.add(p)
    db.session.commit()
    return jsonify({
            "id": p.id,
            'category_id': p.category_id,
            'name': p.name,
            'description': p.description,
            'price': p.price,
            'image': HOST + url_for('product.uploads',filename=p.image)
        })


@blueprint.route('/product/<int:id>', methods=["PUT"])
def update_product(id):
    p = Product.query.get(id)
    category_id = int(request.form.get('category_id', "").strip())
    name = request.form.get('name', "").strip()
    description = request.form.get('description', "").strip()
    price = request.form.get('price', "").strip()
    image = request.files.get("image","")

    p.category_id = category_id
    p.name = name
    p.description = description
    p.price = price
    if image:
        image.save(os.path.join(UPLOADS_DIR, image.filename))
        p.image = image.filename
    db.session.commit()
    return jsonify({
            "id": p.id,
            'category_id': p.category_id,
            'name': p.name,
            'description': p.description,
            'price': p.price,
            'image': HOST + url_for('product.uploads',filename=p.image)
        })

@blueprint.route('/product/<int:id>', methods=["DELETE"])
def delete_product(id):
    p = Product.query.get(id)
    os.remove(os.path.join(UPLOADS_DIR, p.image))
    db.session.delete(p)
    db.session.commit()
    p = {
            "id": p.id,
            'category_id': p.category_id,
            'name': p.name,
            'description': p.description,
            'price': p.price,
        }
    return jsonify(p)
