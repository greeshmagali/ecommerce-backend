from flask import Blueprint,jsonify,request
from models import db,Category,User
from flask_jwt_extended import jwt_required, get_jwt_identity
category_bp=Blueprint("category_bp",__name__)


# helper: only allow admins through
def admin_required():
    user = User.query.get(get_jwt_identity())
    if not user or user.role != "admin":
        return jsonify({
            "message": "admin only"
        }), 403
    return None


@category_bp.route("/categories",methods=["POST"])
@jwt_required()
def add_category():
    error = admin_required()
    if error:
        return error

    data=request.json
    category=Category(
        name=data.get("name")
    )
    db.session.add(category)
    db.session.commit()
    return jsonify({
        "message":"category added successfully"
    }),201


@category_bp.route("/categories",methods=["GET"])
def get_category():
    categories=Category.query.all()
    result=[]
    for category in categories:
        result.append({
            "id":category.id,
            "Name":category.name
        })
    return jsonify(result)
