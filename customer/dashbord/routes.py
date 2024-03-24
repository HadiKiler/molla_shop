from flask import Blueprint, jsonify, request,render_template
from admin.product.models import Product
from admin.category.models import Category
from initialize import db

blueprint = Blueprint('dashbord', __name__)


@blueprint.route('/cart', methods=["GET","POST"])
def cart():
    return render_template('dashbord/cart.html')


@blueprint.route('/checkout', methods=["GET","POST"])
def checkout():
    return render_template('dashbord/checkout.html')


