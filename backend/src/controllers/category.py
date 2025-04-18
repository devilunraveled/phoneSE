from typing import Optional, List

from src import PhoneSELogger
from src.models import Category

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
		category = Category(
			name = data['name'],
			description = data['description'],
			budgetId = data['budgetId'] if 'budgetId' in data else None,
		)

		return category
	except Exception as e:
		PhoneSELogger.error(f"Failed to create category object: {e}")
		return None