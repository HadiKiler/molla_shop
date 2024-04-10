import os
from flask import Blueprint, jsonify, request,url_for
from .models import Product
from initialize import db
from config import UPLOADS_DIR, HOST
from admin.log.models import save_log
from ast import literal_eval
from ..order.models import Order
from datetime import datetime


blueprint = Blueprint('product', __name__)


@blueprint.route('/product', methods=["GET"])
def products():
    sort = literal_eval(request.args.get('sort'))[1]
    start = literal_eval(request.args.get('range'))[0]
    end = literal_eval(request.args.get('range'))[1]
    qs = Product.query.all()

    if sort == "DESC":
        qs = list(qs)
        qs.reverse()

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
    response = jsonify(data[start:end+1])
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
    db.session.add(p)
    db.session.commit()
    image.save(os.path.join(UPLOADS_DIR, image.filename))
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
        try:
            os.remove(os.path.join(UPLOADS_DIR, p.image))
        except:
            pass
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

    count = 0 
    for product in Product.query.all(): # for check products with the same pictures
        if product.image == p.image:
            count+=1
    try:
        if count <= 1: # for check products with the same pictures
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





def calculate_sales(month):
        total_sales = 0
        for order in Order.query.all():
            if order.order_date.month == month:
                total_sales += order.total_amount
        return total_sales

@blueprint.route('/sales_chart')
def sales_chart():
    sales_data = []
    for i in range(1,13):
        sales_data.append({
            'id': i,
            'date': i,
            'sales': calculate_sales(i)
        })
    response = jsonify(sales_data)
    response.headers['Access-Control-Expose-Headers'] = 'Content-Range'
    response.headers['Content-Range'] = len(sales_data)
    return response



@blueprint.route('/product_chart')
def product_chart():
    products = []
    for product in Product.query.all():
        count = 0
        for order in Order.query.all():
            for orderitem in order.orderitems:
                if orderitem.product == product:
                    count += orderitem.quantity
        
        products.append({
            'id':product.id,
            "name": product.name,
            "sales": count
        })
    products  = sorted(products, key=lambda d: d['sales'], reverse=True)
    response = jsonify(products[:5])
    response.headers['Access-Control-Expose-Headers'] = 'Content-Range'
    response.headers['Content-Range'] = len(products)
    return response