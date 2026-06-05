from flask import Flask
from config import Config
from models import db
from flask_jwt_extended import JWTManager
from routes.product_routes import product_bp
from routes.category_routes import category_bp
from routes.cart_routes import cart_bp
from routes.auth import user_bp
from routes.place_order_routes import order_bp
app = Flask(__name__)
app.config.from_object(Config)
jwt = JWTManager(app)
db.init_app(app)
app.register_blueprint(product_bp)
app.register_blueprint(category_bp)
app.register_blueprint(cart_bp)
app.register_blueprint(order_bp)
app.register_blueprint(user_bp)

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)