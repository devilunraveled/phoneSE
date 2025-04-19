import jwt
import os
from flask import request, Response, json, Blueprint
from datetime import datetime, timezone, timedelta
from typing import Optional, List

from src import db, PhoneSELogger
from src.controllers import (
	transaction as transactionController,
	budget as budgetController,
	user as userController
)
from src.models import (
	Transaction,
	Budget,
	BudgetCycle,
	User
)

userBp = Blueprint('user', __name__)

@userBp.route('/register', methods=['POST'])
def registerUser():
	try:
		data = request.get_json()
		if not data:
			return Response(json.dumps({"message": "Input data not provided or invalid"}), status=400, mimetype='application/json')
		
		newUser: Optional[User]
		try:
			newUser = userController.createUser(data)
			if newUser is None:
				raise Exception("Failed to create user object")
		except Exception as e:
			PhoneSELogger.error(f"Failed to create user: {e}")
			return Response(json.dumps({"message": "Failed to create user", "error": str(e)}), 
				   			status=500, 
							mimetype='application/json')	
		db.session.add(newUser)

		token = userController.generateJwtToken(newUser)

		response = json.dumps({
			"message": "User registered successfully",
			"token": newUser.id,
		})

		db.session.commit()

		return Response(response, status=201, mimetype='application/json')
	except Exception as e:
		db.session.rollback()
		PhoneSELogger.error(f"Failed to create user: {e}")
		return Response(json.dumps({"message": "Internal server error", "error": str(e)}), status=500, mimetype='application/json')

@userBp.route('/login', methods=['POST'])
def loginUser():
	try:
		data = request.get_json()
		if not data:
			return Response(json.dumps({"message": "No input data provided"}), status=400, mimetype='application/json')
		
		user: Optional[User]
		try:
			user = userController.validateUser(data)
			if user is None:
				raise Exception("Failed to validate user")
		except Exception as e:
			PhoneSELogger.error(f"Failed to validate user: {e}")
			return Response(json.dumps({"message": "Failed to validate user", "error": str(e)}), 
				   			status=500, 
							mimetype='application/json')

		# generate JWT token
		token = userController.generateJwtToken(user)

		response = json.dumps({
			"message": "Login successful",
			"token": user.id,
		})

		return Response(response, status=200, mimetype='application/json')
	except Exception as e:
		return Response(json.dumps({"message": "An error occurred", "error": str(e)}), status=500, mimetype='application/json')
