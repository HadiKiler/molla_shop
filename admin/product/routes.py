import os
from flask import url_for
from flask import Blueprint, jsonify, request
from .models import Product
from initialize import db
from config import UPLOADS_DIR, HOST
from admin.log.models import save_log


blueprint = Blueprint('product', __name__)


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
            'image': HOST + url_for('uploads',filename=item.image)
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
            'image': HOST + url_for('uploads',filename=p.image)
        })


@blueprint.route('/product', methods=["POST"])
def create_product():
    category_id = int(request.form.get('category_id', "").strip())
    name = request.form.get('name', "").strip()
    description = request.form.get('description', "").strip()
    price = request.form.get('price', "").strip()
    image = request.files.get("image","")

    for product in Product.query.all():
        if product.name == name:
            name+=" Copy"

    p = Product(category_id=category_id, name=name,
                 description=description, price=price,
                 image=image.filename)
    image.save(os.path.join(UPLOADS_DIR, image.filename))
    db.session.add(p)
    db.session.commit()
    save_log(request,f"product {p.id} created !")
    return jsonify({
            "id": p.id,
            'category_id': p.category_id,
            'name': p.name,
            'description': p.description,
            'price': p.price,
            'image': HOST + url_for('uploads',filename=p.image)
        })


@blueprint.route('/product/<int:id>', methods=["PUT"])
def update_product(id):
    category_id = int(request.form.get('category_id', "").strip())
    name = request.form.get('name', "").strip()
    description = request.form.get('description', "").strip()
    price = request.form.get('price', "").strip()
    image = request.files.get("image","")

    products = []
    for product in Product.query.all(): # for exclude current product
        if product.id != id:
            products.append(product)

    for product in products:
        if product.name == name:
            name+=" Copy"
        
    p = Product.query.get(id)
    p.category_id = category_id
    p.name = name
    p.description = description
    p.price = price
    if image:
        image.save(os.path.join(UPLOADS_DIR, image.filename))
        p.image = image.filename
    db.session.commit()
    save_log(request,f"product {id} updated !")
    return jsonify({
            "id": p.id,
            'category_id': p.category_id,
            'name': p.name,
            'description': p.description,
            'price': p.price,
            'image': HOST + url_for('uploads',filename=p.image)
        })

@blueprint.route('/product/<int:id>', methods=["DELETE"])
def delete_product(id):
    p = Product.query.get(id)
    try:
        os.remove(os.path.join(UPLOADS_DIR, p.image))
    except:
        pass
    db.session.delete(p)
    db.session.commit()
    save_log(request,f"product {id} deleted !")
    p = {
            "id": p.id,
            'category_id': p.category_id,
            'name': p.name,
            'description': p.description,
            'price': p.price,
        }
    return jsonify(p)
