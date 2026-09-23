from flask import Blueprint,request,jsonify 
from models import db,Cart, CartItem, Product
from flask_jwt_extended import jwt_required, get_jwt_identity
cart_bp=Blueprint("cart_bp",__name__)


@cart_bp.route("/carts",methods=["POST"])
@jwt_required()
def add_cart():
    data=request.json 
    user_id=get_jwt_identity()
    product_id=data.get("product_id")
    quantity=data.get("quantity")

    # check product exists
    product=Product.query.get(product_id)
    if not product:
        return jsonify({
            "message":"product not found"
        }),404
    
     # check stock
    if quantity >product.stock:
        return jsonify({
            "message":"not enough stock"
        }),400
    
    # check user cart
    cart=Cart.query.filter_by(user_id=user_id).first()

     # create cart if not exists
    if not cart:
        cart = Cart(user_id=user_id)
        db.session.add(cart)
        db.session.commit()

    # check if product already in cart
    cart_item=CartItem.query.filter_by(product_id=product_id,cart_id=cart.id).first()

     # increase quantity
    if cart_item:
        cart_item.quantity+=quantity

    # create new cart item
    else:
        cart_item=CartItem(
            cart_id=cart.id,
            product_id=product_id,
            quantity=quantity
        )
        db.session.add(cart_item)
    db.session.commit()
    return jsonify({
        "message":"product added to cart"
    })



# VIEW CART
@cart_bp.route("/cart/<int:user_id>",methods=["GET"])
@jwt_required()
def get_cart(user_id):
    current_user_id = get_jwt_identity()
    if current_user_id != user_id:
        return jsonify({
            "message":"forbidden"
        }),403

    cart=Cart.query.filter_by(user_id=user_id).first()
    if not cart:
        return jsonify({
            "message":"cart not found"
        }),404
    result=[]
    for item in cart.items:
        result.append({
            "cart_item_id": item.id,
            "product_name": item.product.name,
            "price": item.product.price,
            "quantity": item.quantity,
            "subtotal": item.product.price * item.quantity
        })
    return jsonify(result)


# UPDATE CART ITEM QUANTITY
@cart_bp.route("/cart/item/<int:id>",methods=["PUT"])
@jwt_required()
def update_cart_item(id):
    current_user_id = get_jwt_identity()
    cart_item=CartItem.query.get(id)
    if not cart_item:
        return jsonify({
            "message":"item not found"
        }),404

    if cart_item.cart.user_id != current_user_id:
        return jsonify({
            "message":"forbidden"
        }),403

    data=request.json
    quantity=data.get("quantity")

     # check stock
    if quantity > cart_item.product.stock:
        return jsonify({
            "message": "not enough stock"
        }), 400
    
    # update quantity
    cart_item.quantity=quantity
    db.session.commit()
    return jsonify({
        "message":"cart item updated"
    })



# DELETE CART ITEM
@cart_bp.route("/cart/item/<int:id>",methods=["DELETE"])
@jwt_required()
def delete_cart_item(id):
    current_user_id = get_jwt_identity()
    cart_item=CartItem.query.get(id)
    if not cart_item:
        return jsonify({
            "message":"item not found"
        }),404

    if cart_item.cart.user_id != current_user_id:
        return jsonify({
            "message":"forbidden"
        }),403

    db.session.delete(cart_item)
    db.session.commit()
    return jsonify({
        "message":"item deleted successfully"
    })


    