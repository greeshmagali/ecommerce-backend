from flask import Blueprint, jsonify, request
from models import db, Order, OrderItem, Product, Cart

order_bp = Blueprint("order_bp", __name__)


# PLACE ORDER
@order_bp.route("/order/place", methods=["POST"])
def add_order():

    data = request.json
    user_id = data.get("user_id")

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

    # STEP 3: create order
    order = Order(
        user_id=user_id,
        total_price=total_price,
        status="pending"
    )

    db.session.add(order)
    db.session.commit()

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

    return jsonify({
        "message": "order placed successfully",
        "order_id": order.id,
        "total_price": total_price
    })


# GET ALL ORDERS OF USER
@order_bp.route("/orders/<int:user_id>", methods=["GET"])
def get_orders(user_id):

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
def get_single_order(order_id):

    order = Order.query.get(order_id)

    if not order:
        return jsonify({
            "message": "order not found"
        }), 404

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
