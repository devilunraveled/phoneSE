from datetime import datetime
from typing import List, Optional

from src import PhoneSELogger
from src.models import Transaction
from .category import getCategories
from .account import isValidAccount, getUserAccounts

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
		
		if not isValidAccount(data['payee']) or not isValidAccount(data['payer']):
			PhoneSELogger.error("Invalid payee or payer account")
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
		PhoneSELogger.error(f"Failed to get transaction: {e}")
		return None

def getTransactionsByAccount(accountId: int):
	try:
		transactions: Optional[List[Transaction]] = Transaction.query.filter(Transaction.payee == accountId).all()
		return transactions
	except Exception as e:
		PhoneSELogger.error(f"Failed to get transactions: {e}")
		return None

def getTransactionsByUser(userId: int):
	try:
		transactions: List[Transaction] = []
		accounts = getUserAccounts(userId)
		if accounts is None:
			return None
		
		for account in accounts:
			accTransactions = getTransactionsByAccount(account.id)
			if accTransactions is None:
				return None
			transactions.extend(accTransactions)

		return transactions
	except Exception as e:
		PhoneSELogger.error(f"Failed to get transactions: {e}")
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
