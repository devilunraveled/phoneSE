from flask import Flask
import os
from src.config.config import Config
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
# for password hashing
from flask_bcrypt import Bcrypt

# loading environment variables
load_dotenv()

# declaring flask application
app = Flask(__name__)

# calling the dev configuration
config = Config().dev_config

# making our application to use dev env
app.env = config.ENV

# Path for our local sql lite database
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("SQLALCHEMY_DATABASE_URI")

# To specify to track modifications of objects and emit signals
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = os.environ.get("SQLALCHEMY_TRACK_MODIFICATIONS")

# sql alchemy instance
db = SQLAlchemy(app)

# Flask Migrate instance to handle migrations
migrate = Migrate(app, db)

# import models to let the migrate tool know
from src.models.user import User
from src.models.transaction import Transaction
from src.models.account import Account
from src.models.budget import Budget
from src.models.budgetCycle import BudgetCycle
from src.models.category import Category

# register the api blueprint with the application
from src.routes import api
app.register_blueprint(api, url_prefix='/api')