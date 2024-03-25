import os
from flask import Blueprint, jsonify,request,url_for
from initialize import db
from .models import Category
from admin.log.models import save_log
from config import UPLOADS_DIR, HOST

blueprint = Blueprint('category', __name__)


@blueprint.route('/category', methods=["GET"])
def categories():
    qs = Category.query.all()
    data = []
    for item in qs:
        data.append({
            "id": item.id,
            'name': item.name,
            'create_at': item.create_at,
            'image': HOST + url_for('uploads',filename=item.image)
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
            'create_at': c.create_at,
            'image': HOST + url_for('uploads',filename=c.image)
        })


@blueprint.route('/category', methods=["POST"])
def create_category():
    name = request.form.get('name', "").strip()
    description = request.form.get('description', "").strip()
    image = request.files.get("image","")

    c = Category.query.filter_by(name=name).first()
    if c:
        name = name + " Copy"

    c = Category(name=name, description=description,image=image.filename)
    db.session.add(c)
    db.session.commit()
    image.save(os.path.join(UPLOADS_DIR, image.filename))
    save_log(request,f"category {c.id} created !")
    return jsonify({
            "id": c.id,
            'name': c.name,
            'description': c.description,
            'create_at': c.create_at,
            'image': HOST + url_for('uploads',filename=c.image)
        })


@blueprint.route('/category/<int:id>', methods=["PUT"])
def update_category(id):
    name = request.form.get('name', "").strip()
    description = request.form.get('description', "").strip()
    image = request.files.get("image","")

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
    if image:
        try:
            os.remove(os.path.join(UPLOADS_DIR, c.image))
        except:
            pass
        image.save(os.path.join(UPLOADS_DIR, image.filename))
        c.image = image.filename
    db.session.commit()
    save_log(request,f"category {id} updated !")
    return jsonify({
            "id": c.id,
            'name': c.name,
            'description': c.description,
            'create_at': c.create_at,
            'image': HOST + url_for('uploads',filename=c.image)
        })



@blueprint.route('/category/<int:id>', methods=["DELETE"])
def delete_category(id):
    c = Category.query.get(id)

    count = 0 
    for category in Category.query.all(): # for check categorys with the same pictures
        if category.image == c.image:
            count+=1
    try:
        if count <= 1: # for check categorys with the same pictures
            os.remove(os.path.join(UPLOADS_DIR, c.image))
    except:
        pass
    
    db.session.delete(c)
    db.session.commit()
    save_log(request,f"category {id} deleted !")
    return jsonify({
            "id": c.id,
            'name': c.name,
            'description': c.description,
            'create_at': c.create_at
        })
