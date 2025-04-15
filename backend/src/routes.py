from flask import Blueprint
from src.controllers.user import user_bp

# main blueprint to be registered with application
api = Blueprint('api', __name__)

# register user with api blueprint
api.register_blueprint(user_bp, url_prefix="/user")