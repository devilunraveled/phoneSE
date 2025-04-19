from typing import Optional, List

from src import PhoneSELogger
from src.models import Category
from .user import checkIfUserExists

def getCategories(categoryIds: List[int]) -> Optional[List[Category]]:
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

def createCategory(data) -> Optional[Category]:
	try:
		if not checkIfUserExists(data['userId']):
			PhoneSELogger.error("User does not exist")
			return None

		category = Category(
			name = data['name'],
			description = data['description'],
			budgetId = data['budgetId'] if 'budgetId' in data else None,
			userId = data['userId']
		)

		return category
	except Exception as e:
		PhoneSELogger.error(f"Failed to create category object: {e}")
		return None

def getUserCategories(userId: int) -> Optional[List[Category]]:
	try:
		categories = Category.query.filter_by(userId=userId).all()
		return categories
	except Exception as e:
		PhoneSELogger.error(f"Failed to get categories: {e}")
		return None