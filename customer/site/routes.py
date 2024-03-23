from flask import Blueprint, jsonify, request,render_template
from admin.product.models import Product
from admin.category.models import Category
from initialize import db
from ast import literal_eval

blueprint = Blueprint('site', __name__)


@blueprint.route('/', methods=["GET"])
def main():
    context = {}
    context['categories'] = Category.query.all()

    beautiful_products = list(Product.query.order_by('price'))
    beautiful_products.reverse()
    beautiful_products = beautiful_products[:10]
    context['beautiful_products'] = beautiful_products

    last_prodcuts = list(Product.query.all())
    last_prodcuts.reverse()
    last_prodcuts = last_prodcuts[:10]
    context['last_products'] = last_prodcuts
    
    return render_template('site/main.html',**context)


@blueprint.route('/shop', methods=["GET"])
def shop():
    context = {}
    products =  Product.query.all()
    context['products'] = products
    context['categories'] = Category.query.all()

    return render_template('site/shop.html',**context)

@blueprint.route('/about-us', methods=["GET"])
def about_us():
    return render_template("site/about.html")