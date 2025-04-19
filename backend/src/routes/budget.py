from flask import request, Response, json, Blueprint
from typing import Optional, List

from src import db, PhoneSELogger
from src.controllers import (
    budget as budgetController,
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

        budget: Optional[Budget]
        try:
            budget = budgetController.createBudget(**data)
            if budget is None:
                raise Exception("Failed to create budget object")
        except Exception as e:
            PhoneSELogger.error(f"Failed to create budget: {e}")
            return Response(json.dumps({"message": "Failed to create budget", "error": str(e)}), status=500, mimetype='application/json')

        db.session.add(budget)
        db.session.commit()

        return Response(json.dumps({"message": "Budget created successfully"}), status=200, mimetype='application/json')
    except Exception as e:
        db.session.rollback()
        PhoneSELogger.error(f"Failed to create budget: {e}")
        return Response(json.dumps({"message": "Internal server error", "error": str(e)}), status=500, mimetype='application/json')
