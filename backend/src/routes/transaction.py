from flask import request, Response, json, Blueprint
from typing import Optional, List

from src import db, PhoneSELogger
from src.controllers import (
        transaction as transactionController,
        budget as budgetController,
        )
from src.models import (
        Transaction,
        Budget,
        BudgetCycle
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

        # Get relevant budgets
        relevantBudgets: List[Budget]
        try:
            relevantBudgets = budgetController.getRelevantBudgets(transaction)
            if relevantBudgets is None:
                raise Exception("Failed to get relevant budgets")
        except Exception as e:
            PhoneSELogger.error(f"Failed to get budgets: {e}")
            return Response(json.dumps({"message": "Failed to get relevant budgets", "error": str(e)}), 
                            status=500, 
                            mimetype='application/json')

        # Get active budget cycles
        budgetCycles: List[BudgetCycle]
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

        # Add transaction to respective budget cycles
        for budgetCycle in budgetCycles:
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
