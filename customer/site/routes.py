from flask import Blueprint, jsonify, request,render_template
from admin.product.models import Product
from initialize import db
from ast import literal_eval

blueprint = Blueprint('site', __name__)


@blueprint.route('/', methods=["GET"])
def main():
    return render_template('site/main.html')
