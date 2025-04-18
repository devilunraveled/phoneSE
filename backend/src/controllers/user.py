from flask import request, Response, json, Blueprint
from src.models.user import User
from src import bcrypt, db
from datetime import datetime, timezone, timedelta
import jwt
import os

# creating a blueprint for user routes
userBp = Blueprint('user', __name__)

#HEAD
def checkIfUserExists(userId):
    user = User.query.filter_by(id=userId).first()
    if not user:
        return False
    return True

# user registration route
@userBp.route('/register', methods=['POST'])
def register_user():
    try :
        data = request.get_json()
        if not data:
            return Response(json.dumps({"message": "No input data provided"}), status=400, mimetype='application/json')

        firstName = data.get('firstName')
        lastName = data.get('lastName')
        callingCode = data.get('callingCode')
        phoneNumber = data.get('phoneNumber')
        password = data.get('password')

        if not phoneNumber or not callingCode:
            return Response(json.dumps({"message": "Missing required fields"}), status=400, mimetype='application/json')

        # check if user already exists
        existing_user = User.query.filter_by(phoneNumber=phoneNumber).first()
        if existing_user:
            return Response(json.dumps({"message": "User already exists"}), status=400, mimetype='application/json')

        # hash the password
        hashedPassword = bcrypt.generate_password_hash(password).decode('utf-8')

        # create a new user
        new_user = User(
            firstName=firstName,
            lastName=lastName,
            callingCode=callingCode,
            phoneNumber=phoneNumber,
            passwordHash=hashedPassword
        )
        db.session.add(new_user)

        payload = {
            'iat': datetime.now(timezone.utc),
            'user_id': str(new_user.id),
            'firstName': new_user.firstName,
            'lastName': new_user.lastName,
            'phoneNumber': new_user.phoneNumber,
            'exp': datetime.now(timezone.utc) + timedelta(days=1)
        }
        token = jwt.encode(payload, os.getenv('SECRET_KEY'), algorithm='HS256')

        response = json.dumps({
            "message": "User registered successfully",
            "token": token,
        })

        db.session.commit()

        return Response(response, status=201, mimetype='application/json')
    except Exception as e:
        db.session.rollback()
        return Response(json.dumps({"message": "An error occurred", "error": str(e)}), status=500, mimetype='application/json')
    
# user login route
@userBp.route('/login', methods=['POST'])
def login_user():
    try:
        data = request.get_json()
        if not data:
            return Response(json.dumps({"message": "No input data provided"}), status=400, mimetype='application/json')

        phoneNumber = data.get('phoneNumber')
        password = data.get('password')

        if not phoneNumber or not password:
            return Response(json.dumps({"message": "Missing required fields"}), status=400, mimetype='application/json')

        # check if user exists
        user = User.query.filter_by(phoneNumber=phoneNumber).first()
        if not user:
            return Response(json.dumps({"message": "User does not exist"}), status=404, mimetype='application/json')

        # check if password is correct
        if not bcrypt.check_password_hash(user.passwordHash, password):
            return Response(json.dumps({"message": "Invalid password"}), status=401, mimetype='application/json')

        # generate JWT token
        payload = {
            'iat': datetime.now(timezone.utc),
            'user_id': str(user.id),
            'firstName': user.firstName,
            'lastName': user.lastName,
            'phoneNumber': user.phoneNumber,
            'exp': datetime.now(timezone.utc) + timedelta(days=1)
        }
        token = jwt.encode(payload,os.getenv('SECRET_KEY'),algorithm='HS256')

        response = json.dumps({
            "message": "Login successful",
            "token": token,
        })

        return Response(response, status=200, mimetype='application/json')
    except Exception as e:
        return Response(json.dumps({"message": "An error occurred", "error": str(e)}), status=500, mimetype='application/json')
