from flask import request, Response, json, Blueprint
from datetime import datetime

from src import db
from src.models.transaction import Transaction
from .category import getCategories

transactionBp = Blueprint('transaction', __name__)

# POST
@transactionBp.route('/create', methods=['POST'])
def createTransaction():
	"""
	1. Create transaction object with the details provided in request.
	2. Add the transaction to the relevant budget cycles.
	3. Commit the updated budget cycles to database.
	4. If this was unsuccessful, return error. 
	   Otherwise, commit transaction to database and return success.
	"""
	try:
		data = request.get_json()
		if not data:
			return Response(json.dumps({"message": "Input data not provided or invalid"}), status=400, mimetype='application/json')

		categoryIds = data['categories']
		if not categoryIds:
			categoryIds = []
		
		categories: list
		try:
			categories = getCategories(categoryIds)
		except Exception as e:
			return Response(json.dumps({"message": "Internal server error: failed to get categories", "error": str(e)}), 
				   			status=500, 
							mimetype='application/json')

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

		db.session.add(transaction)
		db.session.commit()

		return Response(json.dumps({"message": "Transaction created successfully"}), status=201, mimetype='application/json')
	except Exception as e:
		return Response(json.dumps({"message": "Internal server error", "error": str(e)}), status=500, mimetype='application/json')

# GET
@transactionBp.route('/get/<int:id>', methods=['GET'])
def getTransaction(id: int):
	try:
		transaction: Transaction | None = Transaction.query.get(id)
		if transaction is None:
			return Response(json.dumps({"message": "Transaction does not exist"}), 
				   			status=404,
							mimetype='application/json')
		
		response = json.jsonify(transaction)
		
		# ? how to jsonify db.Model object
		return response
	
	except Exception as e:
		return Response(json.dumps({"message": "Internal server error", "error": str(e)}), status=500, mimetype='application/json')

# PUT
@transactionBp.route('/update/<int:id>', methods=['PUT'])
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
@transactionBp.route('/delete/<int:id>', methods=['DELETE'])
def deleteTransaction(id: int):
	pass
