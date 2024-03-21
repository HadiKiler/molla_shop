import base64, os
from flask import Blueprint, request, jsonify
from admin.user.models import User
from config import UPLOADS_DIR
blueprint = Blueprint('auth', __name__)



@blueprint.route('/admin/login',methods=["POST"])
def login():
    username = request.json.get('username').strip()
    password = request.json.get('password').strip()
    user = User.query.filter_by(username=username).first()
    if user and user.password == password and user.is_admin:
        with open(os.path.join(UPLOADS_DIR, user.image), "rb") as file:
            image = base64.b64encode(file.read()).decode('utf-8')
            return jsonify({
                'id':user.id,
                'fullName':user.username,
                'avatar':"data:image/jpeg;base64,"+image
                }) , 200
    return ({"message":"username or password error"}) , 401