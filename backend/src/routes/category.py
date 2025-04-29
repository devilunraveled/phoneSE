from flask import request, Response, json, Blueprint
from typing import Optional, List

from src import db, PhoneSELogger
from src.controllers import (
	category as categoryController,
	user as userController
)
from src.models import (
	Category,
)

categoryBp = Blueprint('category', __name__)

@categoryBp.route('/create', methods=['POST'])
def createCategory():
	try:
		data = request.get_json()
		if not data:
			return Response(json.dumps({"message": "Input data not provided or invalid"}), status=400, mimetype='application/json')
		
		userId: int
		try:
			userId = userController.getUserIdFromToken(request.headers['Authorization'])
			if userId is None:
				raise Exception("Invalid token")
		except Exception as e:
			PhoneSELogger.error(f"Failed to get user ID from token: {e}")
			return Response(json.dumps({"message": "Failed to decode user token", "error": str(e)}), status=500, mimetype='application/json')
		data['userId'] = userId

		category: Optional[Category]
		try:
			category = categoryController.createCategory(data)
			if category is None:
				raise Exception("Failed to create category object")
		except Exception as e:
			PhoneSELogger.error(f"Failed to create category: {e}")
			return Response(json.dumps({"message": "Failed to create category", "error": str(e)}),
				   			status=500,
							mimetype='application/json')
		
		db.session.add(category)
		db.session.commit()

		return Response(json.dumps({"message": "Category created successfully"}), status=200, mimetype='application/json')
	except Exception as e:
		db.session.rollback()
		PhoneSELogger.error(f"Failed to create category: {e}")
		return Response(json.dumps({"message": "Internal server error", "error": str(e)}), status=500, mimetype='application/json')

@categoryBp.route('/getByUser', methods=['GET'])
def getUserCategories():
	try:
		userId: int
		try:
			userId = userController.getUserIdFromToken(request.headers['Authorization'])
			if userId is None:
				raise Exception("Invalid token")
		except Exception as e:
			PhoneSELogger.error(f"Failed to get user ID from token: {e}")
			return Response(json.dumps({"message": "Failed to decode user token", "error": str(e)}), status=500, mimetype='application/json')
		
		categories: Optional[List[Category]]
		try:
			categories = categoryController.getUserCategories(userId)
			if categories is None:
				raise Exception("Failed to get categories object")
		except Exception as e:
			PhoneSELogger.error(f"Failed to get categories: {e}")
			return Response(json.dumps({"message": "Failed to get categories", "error": str(e)}), status=500, mimetype='application/json')

		response = json.jsonify({"categories": categories})
		return response

	except Exception as e:
		PhoneSELogger.error(f"Failed to get categories: {e}")
		return Response(json.dumps({"message": "Internal server error", "error": str(e)}), status=500, mimetype='application/json')
