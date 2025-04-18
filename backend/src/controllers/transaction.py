from datetime import datetime
from typing import List, Optional

from src import PhoneSELogger
from src.models import Transaction
from .category import getCategories

# POST
def createTransaction(data) -> Optional[Transaction]:
    try:
        categoryIds = data['categories']
        if not categoryIds:
            categoryIds = []

        categories: List
        try:
            categories = getCategories(categoryIds)
        except Exception as e:
            PhoneSELogger.error(f"Failed to get categories: {e}")
            return None

        transaction = Transaction(
                amount = data['amount'],
                currency = data['currency'],
                payee = data['payee'],
                payer = data['payer'],
                name = data['name'],
                description = data['description'],
                timestamp=datetime.now(),
                )
        PhoneSELogger.info(f"Created transaction object: {transaction}")
        transaction.categories.extend(categories)

        return transaction
    except Exception as e:
        PhoneSELogger.error(f"Failed to create transaction object: {e}")
        return None

# GET
def getTransaction(id: int):
    try:
        transaction: Optional[Transaction] = Transaction.query.get(id)
        return transaction	
    except Exception as e:
		return None

# PUT
def updateTransaction(id: int):
	pass

# PATCH
def updateName():
	pass

def updateDescription():
	pass

def updateAmount():
	pass

def updateCurrency():
	pass

def updateTimestamp():
	pass

def updateCategory():
	pass

# DELETE
def deleteTransaction(id: int):
	pass
