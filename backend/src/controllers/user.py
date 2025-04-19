import jwt
import os
from datetime import datetime, timezone, timedelta
from typing import Optional

from src import bcrypt, db, PhoneSELogger
from src.controllers.budget import getBudget
from src.models import User

def checkIfUserExists(userId):
    user = User.query.filter_by(id=userId).first()
    if not user:
        return False
    return True

def createUser(data) -> Optional[User]:
    try:
        firstName = data.get('firstName')
        lastName = data.get('lastName')
        countryCode = data.get('countryCode')
        phoneNumber = data.get('phoneNumber')
        password = data.get('password')

        if not phoneNumber or not countryCode:
            PhoneSELogger.error("Phone number or calling code not provided")
            return None

        # check if user already exists
        existing_user = User.query.filter_by(phoneNumber=phoneNumber).first()
        if existing_user:
            PhoneSELogger.error(f"User with phone number {phoneNumber} already exists")
            return None

        # hash the password
        hashedPassword = bcrypt.generate_password_hash(password).decode('utf-8')

        # create a new user

        newUser = User(
            firstName=firstName,
            lastName=lastName,
            countryCode=countryCode,
            phoneNumber=phoneNumber,
            passwordHash=hashedPassword
        )

        return newUser
    except Exception as e:
        PhoneSELogger.error(f"Failed to create user: {e}")
        return None

def validateUser(data) -> Optional[User]:
    phoneNumber = data.get('phoneNumber')
    password = data.get('password')

    if not phoneNumber or not password:
        PhoneSELogger.error("Phone number or password not provided")
        raise Exception("Phone number or password not provided")
    
    # check if user exists
    user: Optional[User] = User.query.filter_by(phoneNumber=phoneNumber).first()
    if not user:
        PhoneSELogger.error(f"User with phone number {phoneNumber} does not exist")
        raise Exception("User does not exist")

    # check if password is correct
    if not bcrypt.check_password_hash(user.passwordHash, password):
        raise Exception("Invalid password")

    return user

def generateJwtToken(user: User):
    payload = {
        'iat': datetime.now(timezone.utc),
        'userId': str(user.id),
        'firstName': user.firstName,
        'lastName': user.lastName,
        'phoneNumber': user.phoneNumber,
        'exp': datetime.now(timezone.utc) + timedelta(days=1)
    }
    token = jwt.encode(payload, os.getenv('SECRET_KEY'), algorithm='HS256')
    return token

def decodeJwtToken(token: str):
    try:
        payload = jwt.decode(token, os.getenv('SECRET_KEY'), algorithms=['HS256'])
        PhoneSELogger.info("Decoded token.")
        return payload
    except jwt.ExpiredSignatureError:
        PhoneSELogger.error("Token has expired")
        return None
    except jwt.InvalidTokenError:
        PhoneSELogger.error("Invalid token")
        return None

def getUserIdFromToken(token: str) -> Optional[int]:
    try:
        payload = jwt.decode(token, os.getenv('SECRET_KEY'), algorithms=['HS256'])
        return payload['userId']
    except Exception as e:
        PhoneSELogger.error(f"Failed to get user ID from token: {e}")
        return None

