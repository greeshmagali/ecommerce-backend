from flask import Blueprint,jsonify,request
from models import db,Category
category_bp=Blueprint("category_bp",__name__)


@category_bp.route("/categories",methods=["POST"])
def add_category():
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
