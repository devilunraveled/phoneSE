from flask import Blueprint

from src.routes.user import userBp
from src.routes.transaction import transactionBp
from src.routes.category import categoryBp
from src.routes.account import accountBp

# main blueprint to be registered with application
api = Blueprint('api', __name__)

# register user with api blueprint
api.register_blueprint(userBp, url_prefix="/user")
api.register_blueprint(transactionBp, url_prefix="/transaction")
api.register_blueprint(categoryBp, url_prefix="/category")
api.register_blueprint(accountBp, url_prefix="/account")
