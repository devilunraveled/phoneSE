from flask import request, Response, json, Blueprint
from typing import Optional, List

from src import db, PhoneSELogger
from src.controllers import (
        transaction as transactionController,
        budget as budgetController,
        user as userController,
        account as accountController
        )
from src.models import (
        Transaction,
        Budget,
        BudgetCycle,
        Account
        )

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

        transaction: Optional[Transaction]
        try:
            transaction = transactionController.createTransaction(data)
            if transaction is None:
                raise Exception("Failed to create transaction object")
        except Exception as e:
            PhoneSELogger.error(f"Failed to create transaction: {e}")
            return Response(json.dumps({"message": "Failed to create transaction", "error": str(e)}), 
                            status=500, 
                            mimetype='application/json')
        
        # Debit from payer account
        payerAccount: Optional[Account]
        try:
            payerAccount = accountController.debitAccount(transaction.payer, transaction.amount, transaction.currency)
            if payerAccount is None:
                raise Exception("Failed to get payer account")
        except Exception as e:
            PhoneSELogger.error(f"Failed to get payer account: {e}")
            return Response(json.dumps({"message": "Failed to get payer account", "error": str(e)}), 
                            status=500, 
                            mimetype='application/json')
        
        # Credit to payer account
        payeeAccount: Optional[Account]
        try:
            payeeAccount = accountController.creditAccount(transaction.payee, transaction.amount, transaction.currency)
            if payeeAccount is None:
                raise Exception("Failed to debit payee account")
        except Exception as e:
            PhoneSELogger.error(f"Failed to debit payee account: {e}")
            return Response(json.dumps({"message": "Failed to debit payee account", "error": str(e)}), 
                            status=500, 
                            mimetype='application/json')

        try:
            relevantBudgets = budgetController.getRelevantBudgets(transaction)
            if relevantBudgets is None:
                raise Exception("Failed to get relevant budgets")
        except Exception as e:
            PhoneSELogger.error(f"Failed to get budgets: {e}")
            return Response(json.dumps({"message": "Failed to get relevant budgets", "error": str(e)}), 
                            status=500, 
                            mimetype='application/json')
        # print(relevantBudgets)

        try:
            budgetCycles = [ budgetController.getActiveBudgetCycle(budget) for budget in relevantBudgets]
            
            if (any( budgetCycle is None for budgetCycle in budgetCycles ) ):
                raise Exception("Failed to get active budget cycles")
            
            if budgetCycles is None:
                raise Exception("Failed to get budget cycles")
        except Exception as e:
            PhoneSELogger.error(f"Failed to get budget cycles: {e}")
            return Response(json.dumps({"message": "Failed to get budget cycles", "error": str(e)}), 
                            status=500, 
                            mimetype='application/json')
        # print(budgetCycles)

        # Add transaction to respective budget cycles
        for budgetCycle in budgetCycles:
            if budgetCycle is None:
                PhoneSELogger.critical("Budget Cycle found None despite checking.")
                continue
            budgetCycle.transactions.append(transaction)

        db.session.add(transaction)

        db.session.commit() # automatically commits all budget cycle changes as well
        return Response(json.dumps({"message": "Transaction created successfully"}), 
                        status=200, 
                        mimetype='application/json')

    except Exception as e:
        PhoneSELogger.error(f"Failed to create transaction: {e}")
        db.session.rollback()
        return Response(json.dumps({"message": "Internal server error", "error": str(e)}), status=500, mimetype='application/json')

@transactionBp.route('/get/<int:id>', methods=['GET'])
def getTransaction(id: int):
    try:
        transaction: Optional[Transaction]
        try:
            transaction = transactionController.getTransaction(id)
            if transaction is None:
                raise Exception("Failed to get transaction object")
        except Exception as e:
            PhoneSELogger.error(f"Failed to get transaction: {e}")
            return Response(json.dumps({"message": "Failed to get transaction", "error": str(e)}), 
                            status=500, 
                            mimetype='application/json')

        response = json.jsonify(transaction)
        return response

    except Exception as e:
        PhoneSELogger.error(f"Failed to get transaction: {e}")
        return Response(json.dumps({"message": "Internal server error", "error": str(e)}), status=500, mimetype='application/json')

@transactionBp.route('/getByAccount/<int:accountId>', methods=['GET'])
def getTransactionsByAccount(accountId: int):
    try:
        transactions: Optional[List[Transaction]]
        try:
            transactions = transactionController.getTransactionsByAccount(accountId)
            if transactions is None:
                raise Exception("Failed to get transactions object")
        except Exception as e:
            PhoneSELogger.error(f"Failed to get transactions: {e}")
            return Response(json.dumps({"message": "Failed to get transactions", "error": str(e)}), 
                            status=500, 
                            mimetype='application/json')

        response = json.jsonify({"transactions": transactions})
        return response

    except Exception as e:
        PhoneSELogger.error(f"Failed to get transactions: {e}")
        return Response(json.dumps({"message": "Internal server error", "error": str(e)}), status=500, mimetype='application/json')

@transactionBp.route('/getByUser', methods=['GET'])
def getTransactionsByUser():
    try:
        userId: int
        try:
            userId = userController.getUserIdFromToken(request.headers['Authorization'])
            if userId is None:
                raise Exception("Invalid token")
        except Exception as e:
            PhoneSELogger.error(f"Failed to get user ID from token: {e}")
            return Response(json.dumps({"message": "Failed to decode user token", "error": str(e)}), status=500, mimetype='application/json')
        
        transactions: Optional[List[Transaction]]
        try:
            transactions = transactionController.getTransactionsByUser(userId)
            if transactions is None:
                raise Exception("Failed to get transactions object")
        except Exception as e:
            PhoneSELogger.error(f"Failed to get transactions: {e}")
            return Response(json.dumps({"message": "Failed to get transactions", "error": str(e)}), 
                            status=500, 
                            mimetype='application/json')

        response = json.jsonify({"transactions": transactions})

        return response
    except Exception as e:
        PhoneSELogger.error(f"Failed to get transactions: {e}")
        return Response(json.dumps({"message": "Internal server error", "error": str(e)}), status=500, mimetype='application/json')
