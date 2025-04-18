from flask import request, Response, json, Blueprint
from datetime import datetime

from src import db
from src.models.category import Category

categoryBp = Blueprint('category', __name__)

def getCategories(categoryIds: list[int]):
	if len(categoryIds) == 0:
		return []

	try:
		categoryList = Category.query.filter(Category.id.in_(categoryIds)).all()
		if not categoryList:
			raise Exception("No categories found")
		
		if len(categoryList) != len(categoryIds):
			raise Exception("Invalid category ids provided")
		
		return categoryList

	except Exception as e:
		raise e

@categoryBp.route('/create', methods=['POST'])
def createCategory():
	try:
		data = request.get_json()

		if not data:
			return Response(json.dumps({"message": "Input data not provided or invalid"}), status=400, mimetype='application/json')
		
		category = Category(
			name = data['name'],
			description = data['description'],
			budgetId = data['budgetId'] if 'budgetId' in data else None,
		)

		db.session.add(category)
		db.session.commit()

		return Response(json.dumps({"message": "Category created successfully"}), status=200, mimetype='application/json')
	except Exception as e:
		return Response(json.dumps({"message": "Internal server error", "error": str(e)}), status=500, mimetype='application/json')