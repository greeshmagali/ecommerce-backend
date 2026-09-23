from flask import Blueprint, jsonify, request
from models import db, Order, OrderItem, Product, Cart
from flask_jwt_extended import jwt_required, get_jwt_identity

order_bp = Blueprint("order_bp", __name__)


# PLACE ORDER
@order_bp.route("/order/place", methods=["POST"])
@jwt_required()
def add_order():

    user_id = get_jwt_identity()

    # STEP 1: get user cart
    cart = Cart.query.filter_by(user_id=user_id).first()

    if not cart or not cart.items:
        return jsonify({
            "message": "cart is empty"
        }), 400

    total_price = 0

    # STEP 2: check stock + calculate total
    for item in cart.items:

        product = Product.query.get(item.product_id)

        if item.quantity > product.stock:
            return jsonify({
                "message": f"not enough stock for {product.name}"
            }), 400

        total_price += product.price * item.quantity

    try:
        # STEP 3: create order
        order = Order(
            user_id=user_id,
            total_price=total_price,
            status="pending"
        )

        db.session.add(order)
        db.session.flush()

        # STEP 4: move cart items → order items
        for item in cart.items:

            product = Product.query.get(item.product_id)

            order_item = OrderItem(
                order_id=order.id,
                product_id=product.id,
                quantity=item.quantity,
                price=product.price
            )

            # reduce stock
            product.stock -= item.quantity

            db.session.add(order_item)

        # STEP 5: clear cart
        for item in cart.items:
            db.session.delete(item)

        db.session.commit()

    except Exception:
        db.session.rollback()
        return jsonify({
            "message": "order could not be placed, please try again"
        }), 500

    return jsonify({
        "message": "order placed successfully",
        "order_id": order.id,
        "total_price": total_price
    })


# GET ALL ORDERS OF USER
@order_bp.route("/orders/<int:user_id>", methods=["GET"])
@jwt_required()
def get_orders(user_id):

    current_user_id = get_jwt_identity()
    if current_user_id != user_id:
        return jsonify({
            "message": "forbidden"
        }), 403

    orders = Order.query.filter_by(user_id=user_id).all()

    result = []

    for order in orders:

        result.append({
            "order_id": order.id,
            "total_price": order.total_price,
            "status": order.status
        })

    return jsonify(result)


# GET SINGLE ORDER DETAILS
@order_bp.route("/order/<int:order_id>", methods=["GET"])
@jwt_required()
def get_single_order(order_id):

    current_user_id = get_jwt_identity()

    order = Order.query.get(order_id)

    if not order:
        return jsonify({
            "message": "order not found"
        }), 404

    if order.user_id != current_user_id:
        return jsonify({
            "message": "forbidden"
        }), 403

    items = []

    for item in order.order_items:

        items.append({
            "product_name": item.product.name,
            "quantity": item.quantity,
            "price": item.price,
            "subtotal": item.price * item.quantity
        })

    return jsonify({
        "order_id": order.id,
        "total_price": order.total_price,
        "status": order.status,
        "items": items
    })
