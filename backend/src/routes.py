from flask import Blueprint
from src.controllers.user import userBp
from src.controllers.transaction import transactionBp
from src.controllers.category import categoryBp

# main blueprint to be registered with application
api = Blueprint('api', __name__)

# register user with api blueprint
api.register_blueprint(userBp, url_prefix="/user")
api.register_blueprint(transactionBp, url_prefix="/transaction")
api.register_blueprint(categoryBp, url_prefix="/category")
