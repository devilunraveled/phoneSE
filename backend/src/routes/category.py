from flask import request, Response, json, Blueprint
from typing import Optional, List

from src import db, PhoneSELogger
from src.controllers import (
	category as categoryController,
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