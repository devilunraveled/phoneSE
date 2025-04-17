from flask import request, Response, json, Blueprint

from src.models.transaction import Transaction

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
	pass

# GET
@transactionBp.route('/get/<int:id>', methods=['GET'])
def getTransaction(id: int):
	try:
		transaction: Transaction | None = Transaction.query.get(id)
		if transaction is None:
			return Response(json.dumps({"message": "Transaction does not exist"}), 
				   			status=404,
							mimetype='application/json')
		
		# ? how to jsonify db.Model object
		return Response(json.jsonify(transaction),
				  		status=200,
						mimetype='application/json')	
	except Exception as e:
		return Response(json.dumps({"message": "Internal server error"}), status=500, mimetype='application/json')

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
