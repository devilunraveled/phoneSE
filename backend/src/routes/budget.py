from flask import request, Response, json, Blueprint
from typing import Optional, List

from src import db, PhoneSELogger
from src.controllers import (
    budget as budgetController,
    user as userController
    )
from src.models import (
    Transaction,
    Budget,
    BudgetCycle
    )

budgetBp = Blueprint('budget', __name__)

# POST
@budgetBp.route('/create', methods=['POST'])
def createBudget():
    """
    1. Create budget object with the details provided in request.
    2. Add the budget to the database.
    3. Commit the updated budget to database.
    4. If this was unsuccessful, return error. 
       Otherwise, commit budget to database and return success.
    """
    try :
        data = request.get_json()
        if not data :
            return Response(json.dumps({"message": "Input data not provided or invalid"}), status=400, mimetype='application/json')
        
        userId : Optional[int]
        try :
            userId = userController.getUserIdFromToken(request.headers['Authorization'])
            if userId is None:
                raise Exception("Invalid token")
        except Exception as e:
            PhoneSELogger.error(f"Failed to create budget: {e}")
            return Response(json.dumps({"message": "Failed to create budget", "error": str(e)}), status=500, mimetype='application/json')
        data['userId'] = userId

        budget: Optional[Budget]
        budgetCycle: Optional[BudgetCycle]
        try:
            budget, budgetCycle = budgetController.createBudget(**data)
            if budget is None or budgetCycle is None:
                raise Exception("Failed to create budget object")
        except Exception as e:
            PhoneSELogger.error(f"Failed to create budget: {e}")
            return Response(json.dumps({"message": "Failed to create budget", "error": str(e)}), status=500, mimetype='application/json')

        db.session.add(budget)
        db.session.add(budgetCycle)
        db.session.commit()

        return Response(json.dumps({"message": "Budget created successfully"}), status=200, mimetype='application/json')
    except Exception as e:
        db.session.rollback()
        PhoneSELogger.error(f"Failed to create budget: {e}")
        return Response(json.dumps({"message": "Internal server error", "error": str(e)}), status=500, mimetype='application/json')

@budgetBp.route('/getByUser', methods=['GET'])
def getUserBudgets():
    try:
        userId: int
        try:
            userId = userController.getUserIdFromToken(request.headers['Authorization'])
            if userId is None:
                raise Exception("Invalid token")
        except Exception as e:
            PhoneSELogger.error(f"Failed to get user ID from token: {e}")
            return Response(json.dumps({"message": "Failed to decode user token", "error": str(e)}), status=500, mimetype='application/json')
        
        budgets: Optional[List[Budget]]
        try:
            budgets = budgetController.getUserBudgets(userId)
            if budgets is None:
                raise Exception("Failed to get budgets by user")
        except Exception as e:
            PhoneSELogger.error(f"Failed to get budgets by user: {e}")
            return Response(json.dumps({"message": "Failed to get budgets by user", "error": str(e)}), status=500, mimetype='application/json')

        return Response(json.dumps(budgets), status=200, mimetype='application/json')
    except Exception as e:
        PhoneSELogger.error(f"Failed to get budgets by user: {e}")
        return Response(json.dumps({"message": "Internal server error", "error": str(e)}), status=500, mimetype='application/json')

