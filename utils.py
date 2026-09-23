from flask_jwt_extended import get_jwt_identity
from models import db, User


def admin_required():
    user_id = get_jwt_identity()

    user = db.session.get(User, user_id)

    if not user:
        return None

    if user.role != "admin":
        return None

    return user