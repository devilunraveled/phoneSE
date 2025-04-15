from flask import request, Response, json, Blueprint
from src.models.user_model import User
from src import bcrypt, db
from datetime import datetime
import jwt
import os

# creating a blueprint for user routes
user_bp = Blueprint('user', __name__)

#HEAD
def checkIfUserExists(userId):
    user = User.query.filter_by(id=userId).first()
    if not user:
        return False
    return True

# user registration route
@user_bp.route('/register', methods=['POST'])
def register_user():
    try :
        data = request.get_json()
        if not data:
            return Response(json.dumps({"message": "No input data provided"}), status=400, mimetype='application/json')

        firstname = data.get('firstname')
        lastname = data.get('lastname')
        calling_code = data.get('calling_code')
        phone_number = data.get('phone_number')
        password = data.get('password')

        if not phone_number or not calling_code:
            return Response(json.dumps({"message": "Missing required fields"}), status=400, mimetype='application/json')

        # check if user already exists
        existing_user = User.query.filter_by(phone_number=phone_number).first()
        if existing_user:
            return Response(json.dumps({"message": "User already exists"}), status=400, mimetype='application/json')

        # hash the password
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        # create a new user
        new_user = User(
            firstname=firstname,
            lastname=lastname,
            calling_code=calling_code,
            phone_number=phone_number,
            password_hash=hashed_password
        )
        db.session.add(new_user)
        db.session.commit()

        payload = {
            'iat': datetime.now(datetime.timezone.utc),
            'user_id': str(new_user.id),
            'firstname': new_user.firstname,
            'lastname': new_user.lastname,
            'phone_number': new_user.phone_number,
            'exp': datetime.now(datetime.timezone.utc) + datetime.timedelta(days=1)
        }
        token = jwt.encode(payload,os.getenv('SECRET_KEY'),algorithm='HS256')

        response = json.dumps({
            "message": "User registered successfully",
            "token": token,
        })

        return Response(response, status=201, mimetype='application/json')
    except Exception as e:
        return Response(json.dumps({"message": "An error occurred", "error": str(e)}), status=500, mimetype='application/json')
    
# user login route
@user_bp.route('/login', methods=['POST'])
def login_user():
    try:
        data = request.get_json()
        if not data:
            return Response(json.dumps({"message": "No input data provided"}), status=400, mimetype='application/json')

        phone_number = data.get('phone_number')
        password = data.get('password')

        if not phone_number or not password:
            return Response(json.dumps({"message": "Missing required fields"}), status=400, mimetype='application/json')

        # check if user exists
        user = User.query.filter_by(phone_number=phone_number).first()
        if not user:
            return Response(json.dumps({"message": "User does not exist"}), status=404, mimetype='application/json')

        # check if password is correct
        if not bcrypt.check_password_hash(user.password_hash, password):
            return Response(json.dumps({"message": "Invalid password"}), status=401, mimetype='application/json')

        # generate JWT token
        payload = {
            'iat': datetime.now(datetime.timezone.utc),
            'user_id': str(user.id),
            'firstname': user.firstname,
            'lastname': user.lastname,
            'phone_number': user.phone_number,
            'exp': datetime.now(datetime.timezone.utc) + datetime.timedelta(days=1)
        }
        token = jwt.encode(payload,os.getenv('SECRET_KEY'),algorithm='HS256')

        response = json.dumps({
            "message": "Login successful",
            "token": token,
        })

        return Response(response, status=200, mimetype='application/json')
    except Exception as e:
        return Response(json.dumps({"message": "An error occurred", "error": str(e)}), status=500, mimetype='application/json')
