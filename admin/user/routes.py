from flask import Blueprint, jsonify, request
from .models import User
from initialize import db
from flask_cors import CORS

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
            'register_data': item.register_data
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
        })


@blueprint.route('/user', methods=["POST"])
def create_user():
    username = request.json.get('username', "")
    password = request.json.get('password', "")
    email = request.json.get('email', "")
    u = User.query.filter_by(username=username).first()
    if u:
        username = username + " Copy"
    u = User(username=username, password=password, email=email)
    db.session.add(u)
    db.session.commit()
    u = {
            "id": u.id,
            'username': u.username,
            'password': u.password,
            'email': u.email,
            'is_admin': u.is_admin,
        }
    return jsonify(u)


@blueprint.route('/user/<int:id>', methods=["PUT"])
def upate_user(id):
    username = request.json.get('username', "")
    password = request.json.get('password', "")
    email = request.json.get('email', "")
    is_admin = bool(request.json.get('is_admin', ""))
    u = User.query.filter_by(username=username).first()
    if u:
        username = username + " Copy"
    u = User.query.get(id)
    u.username = username
    u.password = password
    u.email = email
    u.is_admin = is_admin
    db.session.commit()
    u = {
            "id": u.id,
            'username': u.username,
            'password': u.password,
            'email': u.email,
            'is_admin': u.is_admin,
        }
    return jsonify(u)


@blueprint.route('/user/<int:id>', methods=["DELETE"])
def delete_user(id):
    u = User.query.get(id)
    db.session.delete(u)
    db.session.commit()
    u = {
            "id": u.id,
            'username': u.username,
            'password': u.password,
            'email': u.email,
            'is_admin': u.is_admin,
        }
    return jsonify(u)
