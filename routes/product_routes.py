from flask import Blueprint, jsonify, request
from models import db, Product, User
from flask_jwt_extended import jwt_required, get_jwt_identity

product_bp = Blueprint("product_bp", __name__)


# helper: only allow admins through
def admin_required():
    user = User.query.get(get_jwt_identity())
    if not user or user.role != "admin":
        return jsonify({
            "message": "admin only"
        }), 403
    return None


# ADD PRODUCT
@product_bp.route("/products", methods=["POST"])
@jwt_required()
def add_product():
    error = admin_required()
    if error:
        return error

    data = request.json
    product = Product(
        name=data.get("name"),
        description=data.get("description"),
        price=data.get("price"),
        stock=data.get("stock"),
        image=data.get("image"),
        category_id=data.get("category_id")
    )
    db.session.add(product)
    db.session.commit()
    return jsonify({
        "message": "product added successfully"
    }), 201


# GET ALL PRODUCTS + FILTERING + PAGINATION
@product_bp.route("/products", methods=["GET"])

def get_products():
    # filters
    name = request.args.get("name")
    category_id = request.args.get("category_id", type=int)
    price = request.args.get("price", type=int)

    # pagination
    page = request.args.get("page", 1, type=int)
    per_page = 5
    offset = (page - 1) * per_page

    # start query
    query = Product.query

    # filtering
    if name:
        query = query.filter_by(name=name)

    if category_id:
        query = query.filter_by(category_id=category_id)

    if price:
        query = query.filter_by(price=price)

    # pagination
    total = query.count()
    products = query.limit(per_page).offset(offset).all()

    # response
    result = []
    for product in products:
        result.append({
            "id": product.id,
            "name": product.name,
            "description": product.description,
            "price": product.price,
            "stock": product.stock,
            "image": product.image,
            "category_id": product.category_id
        })
    return jsonify({
        "products": result,
        "page": page,
        "per_page": per_page,
        "total": total
    })


# GET SINGLE PRODUCT
@product_bp.route("/products/<int:id>", methods=["GET"])

def get_single_product(id):
    product = Product.query.get(id)
    if not product:
        return jsonify({
            "message": "product not found"
        }), 404

    return jsonify({
        "id": product.id,
        "name": product.name,
        "description": product.description,
        "price": product.price,
        "stock": product.stock,
        "image": product.image,
        "category_id": product.category_id
    })


# UPDATE PRODUCT
@product_bp.route("/products/<int:id>", methods=["PUT"])
@jwt_required()
def update_product(id):
    error = admin_required()
    if error:
        return error

    product = Product.query.get(id)
    if not product:
        return jsonify({
            "message": "product not found"
        }), 404
    data = request.json

    if "name" in data:
        product.name = data.get("name")

    if "description" in data:
        product.description = data.get("description")

    if "price" in data:
        product.price = data.get("price")

    if "stock" in data:
        product.stock = data.get("stock")

    if "image" in data:
        product.image = data.get("image")

    if "category_id" in data:
        product.category_id = data.get("category_id")

    db.session.commit()
    return jsonify({
        "message": "product updated successfully"
    })


# DELETE PRODUCT
@product_bp.route("/products/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_product(id):
    error = admin_required()
    if error:
        return error

    product = Product.query.get(id)
    if not product:
        return jsonify({
            "message": "product not found"
        }), 404
    db.session.delete(product)
    db.session.commit()
    return jsonify({
        "message": "product deleted successfully"
    })