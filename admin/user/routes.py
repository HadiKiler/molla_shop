import os
from flask import Blueprint, jsonify, request,url_for
from .models import User
from initialize import db
from config import UPLOADS_DIR, HOST
from admin.log.models import save_log

blueprint = Blueprint('user', __name__)


@blueprint.route('/user', methods=["GET"])
def users():
    qs = User.query.all()
    data = []
    for item in qs:
        data.append({
            "id": item.id,
            'username': item.username,
            'password': item.password,
            'email': item.email,
            'is_admin': item.is_admin,
            'register_date': item.register_date,
            'image': HOST + url_for('uploads',filename=item.image)
        })
    response = jsonify(data)
    response.headers['Access-Control-Expose-Headers'] = 'Content-Range'
    response.headers['Content-Range'] = len(data)
    return response


@blueprint.route('/user/<int:id>', methods=["GET"])
def read_user(id):
    u = User.query.get(id)
    return jsonify({
            "id": u.id,
            'username': u.username,
            'password': u.password,
            'email': u.email,
            'is_admin': u.is_admin,
            'image': HOST + url_for('uploads',filename=u.image)
        })


@blueprint.route('/user', methods=["POST"])
def create_user():
    username = request.form.get('username', "").strip()
    password = request.form.get('password', "").strip()
    email = request.form.get('email', "").strip()
    is_admin = bool(request.form.get('is_admin', ""))
    image = request.files.get("image","")

    for user in User.query.all():
        if user.username == username:
            username+=" Copy"

    # exist = True
    # while (exist): # code check users for unique username  method-2
    #     u = User.query.filter_by(username=username).first()
    #     if u:
    #         username += " Copy"
    #         continue
    #     break

    u = User(username=username, password=password,
              email=email,is_admin=is_admin,image=image.filename)
    image.save(os.path.join(UPLOADS_DIR, image.filename))
    db.session.add(u)
    db.session.commit()
    save_log(request,f"user {u.id} created !")
    return jsonify({
            "id": u.id,
            'username': u.username,
            'password': u.password,
            'email': u.email,
            'is_admin': u.is_admin,
            'image': HOST + url_for('uploads',filename=u.image)
        })


@blueprint.route('/user/<int:id>', methods=["PUT"])
def update_user(id):
    username = request.form.get('username', "").strip()
    password = request.form.get('password', "").strip()
    email = request.form.get('email', "").strip()
    is_admin = bool(request.form.get('is_admin', ""))
    image = request.files.get("image","")
    users = []
    for user in User.query.all(): # for exclude current user
        if user.id != id:
            users.append(user)


    for user in users:
        if user.username == username:
            username += " Copy"

    # exist = True # code check users for unique username method-2
    # while (exist):
    #     exist = False
    #     for user in users:
    #         if user.username == username:
    #             username+=" Copy"
    #             exist =True
    #             break
        
    u = User.query.get(id)
    u.username = username
    u.password = password
    u.email = email
    u.is_admin = is_admin
    if image:
        try:
            os.remove(os.path.join(UPLOADS_DIR, u.image))
        except:
            pass
        image.save(os.path.join(UPLOADS_DIR, image.filename))
        u.image = image.filename
    db.session.commit()
    save_log(request,f"user {id} updated !")
    u = {
            "id": u.id,
            'username': u.username,
            'password': u.password,
            'email': u.email,
            'is_admin': u.is_admin,
            'image': HOST + url_for('uploads',filename=u.image)
        }
    return jsonify(u)


@blueprint.route('/user/<int:id>', methods=["DELETE"])
def delete_user(id):
    u = User.query.get(id)
    try:
        os.remove(os.path.join(UPLOADS_DIR, u.image))
    except:
        pass
    db.session.delete(u)
    db.session.commit()
    save_log(request,f"user {id} deleted !")
    u = {
            "id": u.id,
            'username': u.username,
            'password': u.password,
            'email': u.email,
            'is_admin': u.is_admin,
        }
    return jsonify(u)
