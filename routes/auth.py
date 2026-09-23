from flask import Blueprint,jsonify,request
from models import db,User
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
from flask_jwt_extended import create_access_token
from flask_jwt_extended import jwt_required

user_bp=Blueprint("user_bp",__name__)




@user_bp.route("/signup",methods=["POST"])
def add_user():
    data=request.json 
    username=data.get("username")
    password=data.get("password")
    existing_user=User.query.filter_by(username=username).first()
    if existing_user:
        return jsonify({
            "message": "username already exists"
        }),400
    
    hashed_password=generate_password_hash(password)
    user=User(
        username=username,
        password=hashed_password
    )
    db.session.add(user)
    db.session.commit()
    return jsonify({
        "message": "user added successfully"
    }), 201



@user_bp.route("/login",methods=["POST"])
def get_user():
    data=request.json
    username=data.get("username")
    password=data.get("password")
    user=User.query.filter_by(username=username).first()
    if user and check_password_hash(user.password,password):
        token =create_access_token(identity=user.id)
        return jsonify({
            "message": "login successful",
            "Token":token
        })
    return jsonify({
        "message": "invalid username or password"
    }), 401





@user_bp.route("/profile", methods=["GET"])
@jwt_required()
def profile():
     return jsonify({
        "message": "Protected Profile Route"
    })