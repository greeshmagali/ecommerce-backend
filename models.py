from flask_sqlalchemy import SQLAlchemy 
db=SQLAlchemy()
class User(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(200),unique=True)
    password=db.Column(db.String(200))
    role = db.Column(db.String(20), default="customer") #CUSTOMER OR ADMIN
    cart = db.relationship("Cart", backref="user",uselist=False)
    orders=db.relationship("Order",backref="user")
class Product(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(200))
    description=db.Column(db.String(200))
    price=db.Column(db.Integer)
    stock=db.Column(db.Integer)
    image=db.Column(db.String(200))
    category_id=db.Column(db.Integer,db.ForeignKey("category.id"))
    cart_items=db.relationship("CartItem",backref="product")
    order_items=db.relationship("OrderItem",backref="product")
class Category(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(200))
    products = db.relationship("Product", backref="category")
class Cart(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    user_id=db.Column(db.Integer,db.ForeignKey("user.id"))
    items=db.relationship("CartItem",backref="cart")
class CartItem(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    cart_id=db.Column(db.Integer,db.ForeignKey("cart.id"))
    product_id=db.Column(db.Integer,db.ForeignKey("product.id"))
    quantity=db.Column(db.Integer)
class Order(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    user_id=db.Column(db.Integer,db.ForeignKey("user.id"))
    total_price=db.Column(db.Integer)
    status=db.Column(db.String(200))
    order_items=db.relationship("OrderItem",backref="order")
class OrderItem(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    order_id=db.Column(db.Integer,db.ForeignKey("order.id"))
    product_id=db.Column(db.Integer,db.ForeignKey("product.id"))
    quantity=db.Column(db.Integer)
    price=db.Column(db.Integer)