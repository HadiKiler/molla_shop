from flask import Blueprint, jsonify, request,render_template
from admin.product.models import Product
from admin.category.models import Category
from initialize import db

blueprint = Blueprint('auth', __name__)


@blueprint.route('/login', methods=["GET","POST"])
def login():
    return render_template('auth/login.html')


@blueprint.route('/register', methods=["GET","POST"])
def register():
    return render_template('auth/login.html')